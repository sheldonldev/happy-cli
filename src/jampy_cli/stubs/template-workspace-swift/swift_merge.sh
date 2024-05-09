prev_ckpt=v5/checkpoint-200-merged
curr_ckpt=v6/checkpoint-200

CUDA_VISIBLE_DEVICES=0 swift export \
    --model_id_or_path $(pwd)/models/mini_cpm_v_v2_0/output/$prev_ckpt \
    --ckpt_dir $(pwd)/models/mini_cpm_v_v2_0/output/$curr_ckpt \
    --merge_lora true
