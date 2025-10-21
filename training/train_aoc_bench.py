import verifiers as vf

"""
# install
vf-install wiki-search (-p /path/to/environments)

# quick eval
vf-eval aoc_bench (-m model_name in endpoints.py)

inference:
CUDA_VISIBLE_DEVICES=0,1,2,3,4,5 vf-vllm --model willcb/Qwen3-8B \
    --data-parallel-size 6 --enforce-eager --disable-log-requests

training:
CUDA_VISIBLE_DEVICES=6,7 accelerate launch --num-processes 2 \
    --config-file aocbench/training/config/zero3.yaml aocbench/training/train_aoc_bench.py
"""

vf_env = vf.load_environment(env_id="aoc_bench")

model_name = "willcb/Qwen3-8B"
model, tokenizer = vf.get_model_and_tokenizer(model_name)
run_name = "aoc_bench-grpo_" + model_name.split("/")[-1].lower()

training_args = vf.grpo_defaults(run_name=run_name)
training_args.per_device_train_batch_size = 8
training_args.num_generations = 16
training_args.gradient_accumulation_steps = 16
training_args.num_iterations = 1
training_args.num_train_epochs = 5
training_args.max_seq_len = 4096
training_args.max_steps = 500
training_args.save_steps = 100

trainer = vf.GRPOTrainer(
    model=model,
    processing_class=tokenizer,
    env=vf_env,
    args=training_args,
)
trainer.train()
