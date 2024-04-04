import os
from contextlib import nullcontext
import torch
import gradio as gr
import tiktoken
from model import GLMConfig, MiniGLM

# -----------------------------------------

start = '\n'
num_samples = 1
max_new_tokens = 512
temperature = 0.8
top_k = 200
seed = 1234
device = 'cuda:0'
dtype = 'bfloat16' if torch.cuda.is_available() and torch.cuda.is_bf16_supported() else 'float16'
compile_or_not = False
# exec(open('configurator.py').read())

# -----------------------------------------

dirs = gr.components.Textbox(label="What's your dir?", type="text",)
inputs = gr.components.Textbox(label="What's your problem?", type="text",)
outputs = gr.components.Textbox(label="Answer conveys here", type="text",)


torch.manual_seed(seed)
torch.cuda.manual_seed(seed)
device_type = 'cuda' if 'cuda' in device else 'cpu'  # for later use in torch.autocast
torch.backends.cuda.matmul.allow_tf32 = True  # allow tf32 on matmul
torch.backends.cudnn.allow_tf32 = True  # allow tf32 on cudnn
ptdtype = {'float32': torch.float32, 'bfloat16': torch.bfloat16, 'float16': torch.float16}[dtype]
ctx = nullcontext() if device_type == 'cpu' else torch.amp.autocast(device_type=device_type, dtype=ptdtype)

enc = tiktoken.get_encoding("gpt2")
encode = lambda s: enc.encode(s, allowed_special={"<|endoftext|>"})
decode = lambda l: enc.decode(l, errors='ignore')


# encode the beginning of the prompt
def miniglm_bot(start_prompt, out_dir):
    ckpt_path = os.path.join(out_dir, 'ckpt.pt')  # 无需多言
    checkpoint = torch.load(ckpt_path, map_location=device)
    config = GLMConfig(**checkpoint['model_args'])
    model = MiniGLM(config)
    state_dict = checkpoint['model']
    unwanted_prefix = '_orig_mod.'

    for k, v in list(state_dict.items()):
        if k.startswith(unwanted_prefix):
            state_dict[k[len(unwanted_prefix):]] = state_dict.pop(k)
    model.load_state_dict(state_dict)

    model.eval()
    model.to(device)

    start_ids = encode(start_prompt)
    x = (torch.tensor(start_ids, dtype=torch.long, device=device)[None, ...])

    # run generation
    with torch.no_grad():
        with ctx:
            y = model.generate(x, max_new_tokens, temperature=temperature, top_k=top_k)
            output_tokens = y[0].tolist()
            try:
                end_idx = output_tokens.index(50256)
                output_tokens = output_tokens[:end_idx]
            except:
                pass
            outputs_x = decode(output_tokens)
            nsns = outputs_x.split(';')
            if len(nsns) > 1:
                outputs_x = nsns[1]
            else:
                outputs_x = nsns[0]
            outputs_x.replace('=', '')
            outputs_x.replace('？', '：')
            outputs_x.replace(' ', '')
            return outputs_x


interface = gr.Interface(inputs=[inputs, dirs],
                         fn=miniglm_bot,
                         outputs=outputs,
                         title="狗屁不通Miniglm 金庸生成器",
                         description="我只是一个弱小可怜又无助，只有千余条数据训练的模型555",
                         theme=gr.themes.Default(), )
interface.launch(share=True, server_port=7772)
