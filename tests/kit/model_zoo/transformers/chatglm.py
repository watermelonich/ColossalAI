import torch
import transformers

from colossalai.shardformer.modeling.chatglm2_6b.configuration_chatglm import ChatGLMConfig
from colossalai.shardformer.modeling.chatglm2_6b.modeling_chatglm import ChatGLMForConditionalGeneration, ChatGLMModel

from ..registry import ModelAttribute, model_zoo

# ================================
# Register single-sentence ChatGLM
# ================================


def data_gen():
    input_ids = torch.tensor([[5941, 15, 2670, 3543, 632, 2075]], dtype=torch.int64)
    attention_mask = torch.tensor([[1, 1, 1, 1, 1, 1]])
    return dict(input_ids=input_ids, attention_mask=attention_mask)


# define output transform function
output_transform_fn = lambda x: x

# define loss function
loss_fn_for_chatglm_model = lambda x: x.last_hidden_state.sum()
loss_fn = lambda x: x.logits.sum()

config = ChatGLMConfig(num_layers=1,
                       padded_vocab_size=65024,
                       hidden_size=64,
                       num_attention_heads=8,
                       rmsnorm=True,
                       original_rope=True,
                       use_cache=True,
                       torch_dtype=torch.float32)


model_zoo.register(name='transformers_chatglm',
                   model_fn=lambda: ChatGLMModel(config, empty_init=False),
                   data_gen_fn=data_gen,
                   output_transform_fn=output_transform_fn,
                   loss_fn=loss_fn_for_chatglm_model,
                   model_attribute=ModelAttribute(has_control_flow=True))

model_zoo.register(name="transformers_chatglm_for_conditional_generation",
                   model_fn=lambda: ChatGLMForConditionalGeneration(config, empty_init=False),
                   data_gen_fn=data_gen,
                   output_transform_fn=output_transform_fn,
                   loss_fn=loss_fn,
                   model_attribute=ModelAttribute(has_control_flow=True))