# Retrieval-Augmented-QnA

![Workflow](output.png)

Try it yourself:
pip install -r requirements.txt
pip install detectron2@git+https://github.com/facebookresearch/detectron2.git@d1e04565d3bec8719335b88be9e9b961bf3ec464
cd ./app
streamlit run main.py

OR:
docker build -t demopubmedqa .
docker run -it -p 8501:8501 demopubmedqa