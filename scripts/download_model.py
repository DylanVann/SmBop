import gdown;
url = 'https://drive.google.com/u/0/uc?id=1pQvg2sT7h9t_srgmN1nGGMfIPa62U9ag';
output = 'model.tar.gz';
gdown.download(url, output, quiet=False);