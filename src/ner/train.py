# src/ner/train.py
import spacy
from spacy.training import Example

def train_ner():
    nlp = spacy.blank("en")
    ner = nlp.add_pipe("ner")
    
    # 添加实体标签
    for label in ["EMISSION", "BATTERY", "CERTIFICATION"]:
        ner.add_label(label)
    
    # 训练逻辑（示例）
    optimizer = nlp.begin_training()
    for epoch in range(10):
        losses = {}
        for text, annotations in training_data:
            example = Example.from_dict(nlp.make_doc(text), annotations)
            nlp.update([example], losses=losses)
        print(f"Epoch {epoch}, Loss: {losses['ner']}")