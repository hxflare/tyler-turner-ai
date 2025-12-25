import moondream as md
from llama_cpp import Llama
from PIL import Image
import time
from data_manager import Config
config=Config()
class ai:
    def __init__(self):
        self.prompt=config.prompt
        self.moondream = md.vl(model="./ais/moondream-0_5b-int8.mf")
        self.llm=Llama(model_path="./ais/Qwen2.5-3B-Instruct-Uncensored-Test-Q4_K_M.gguf",n_threads=3,verbose=False,n_ctx=2048)
        self.history_gl=[]
    def describe_image(self,image_path:str, verbose:bool=False)->str:
        print(f"describing {image_path}")
        prompt="What is the detailed description of this image?"
        start_time=time.time()
        encoded_image=None
        image=Image.open(image_path)
        encoded_image=self.moondream.encode_image(image)
        print(f"encoded image in {time.time()-start_time}")
        query = self.moondream.query(encoded_image,prompt,stream=False)
        print(f"described image in {time.time()-start_time}, output:{query["answer"]}")
        if verbose: print(query)
        return query["answer"]
    async def respond(self,message:str,user:str="hxflare",image_path:str|None=None,history=None)->list:
        print(f"ai respond to {message}")
        starttime=time.time()
        if history == None: history=self.history_gl
        if image_path==None:
            output = self.llm(f"<|im_start|>chat user {self.prompt}.\n sent a message to you:\n{message}\n<|im_end|><|im_start|>response you respond(with heavy accent on your fetish): ",max_tokens=256,stop=["Message:","Photo:","responds:","#"])
            if history==None:
                self.history_gl.append({"username":user,"message":message,"photo":image_desc,"response":output["choices"][0]["text"]})
            print(f"responded in: {time.time()-starttime} with {output["choices"][0]["text"]}")
            return [output["choices"][0]["text"]]
        else:
            image_desc=self.describe_image(image_path)
            output = self.llm(f"<|im_start|>user {self.prompt}.\n Message:{message}. \nPhoto:{image_desc}\n<|im_end|><|im_start|>response you respond(with heavy accent on your fetish): ",max_tokens=256,stop=["Message:","Photo:","responds:","#"])
            if history==None:
                self.history_gl.append({"username":user,"message":message,"photo":image_desc,"response":output["choices"][0]["text"]})
            print(f"responded in: {time.time()-starttime} with {output["choices"][0]["text"]}")
            return [output["choices"][0]["text"],image_desc]
