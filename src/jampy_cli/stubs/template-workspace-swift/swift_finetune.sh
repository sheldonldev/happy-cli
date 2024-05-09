curr_ckpt=v6/checkpoint-200-merged
future_version=v7
dataset=declaration_table_records

CUDA_VISIBLE_DEVICES=0 swift sft \
    --model_type minicpm-v-v2 \
    --template_type minicpm-v \
    --sft_type lora \
    --model_id_or_path $(pwd)/models/mini_cpm_v_v2_0/output/$curr_ckpt \
    --output_dir $(pwd)/models/mini_cpm_v_v2_0/output/$future_version \
    --logging_dir $(pwd)/models/mini_cpm_v_v2_0/output/$future_version/runs \
    --custom_train_dataset_path $(pwd)/data/$dataset/json/train.json \
    --custom_val_dataset_path $(pwd)/data/$dataset/json/dev.json \
    --batch_size 8 \
    --eval_batch_size 8 \
    --save_steps 200 \
    --learning_rate 1e-04 \
    --lora_target_modules q_proj k_proj v_proj \
    --gradient_accumulation_steps 16 \
    --add_output_dir_suffix False
