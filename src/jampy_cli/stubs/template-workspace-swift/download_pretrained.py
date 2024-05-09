from pathlib import Path

from modelscope import snapshot_download

print('Downloading...')
model_dir = snapshot_download(
    'OpenBMB/MiniCPM-V-2',
    cache_dir=Path(__file__).parent.joinpath('pretrained'),
)
print(model_dir)
print('Downloaded!')
