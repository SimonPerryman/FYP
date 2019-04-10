# FILE TO TRAIN SPACY DATA SET TO ADD ALL FILMS AND CREW MEMEBERS THAT ARE IN THE DATABASE

from random import shuffle
from database import getAllCrewMembersNames, getAllFilms
from pathlib import Path
import spacy
from spacy.util import minibatch, compounding

def split_lists(list_to_split):
    index = int(len(list_to_split) / 5)
    shuffle(list_to_split)
    l1 = list_to_split[:index]
    if index % 2 == 0:
        l2 = list_to_split[index:(2*index)]
        l3 = list_to_split[(2*index):(3*index)]
    else:
        l2 = list_to_split[index:((2*index) + 1)]
        l3 = list_to_split[((2*index) + 1):(3*index)]
    l4 = list_to_split[(3*index):(4*index)]
    l5 = list_to_split[(4*index):]
    return l1, l2, l3, l4, l5

def build_train_data(crew, key, example, start_index, entity_type):
    train_data = []
    for crew_member in crew:
        train_data.append((example.format(crew_member[key].title()), {"entities": [(start_index, start_index + len(crew_member), entity_type)]}))
    return train_data


def get_train_data():
    train_data = []

    crew1, crew2, crew3, crew4, crew5 = split_lists(getAllCrewMembersNames())
    film1, film2, film3, film4, film5 = split_lists(getAllFilms())

    ExC1 = "It is a film with {} in it."
    ExC2 = "Have you seen the movie starring {} and {}."
    ExC3 = "Last a film came out where the lead cast member was {}."
    ExC4 = "Was {} in the film Batman Begins?"
    ExC5 = "I liked {}'s latest film."

    ExF1 = "I liked the film {}."
    ExF2 = "I hated {}."
    ExF3 = "Have you seen {}."
    ExF4 = "Were you a fan of {}?"
    ExF5 = "I would rate {} a 3/10."


    train_data = (build_train_data(crew1, 'Name', ExC1, 18, "PERSON"))
    for idx in range(0, len(crew2), 2):
        train_data.append((ExC2.format(crew2[idx]['Name'].title(), crew2[idx+1]['Name'].title()), {"entities": [
            (33, 33 + len(crew2[idx]), "PERSON"),
            (38 + len(crew2[idx]), 38 + len(crew2[idx]) + len(crew2[idx+1]), "PERSON")
        ]}))
    train_data.extend(build_train_data(crew3, 'Name', ExC3, 52, "PERSON"))
    train_data.extend(build_train_data(crew4, 'Name', ExC4, 4, "PERSON"))
    train_data.extend(build_train_data(crew5, 'Name', ExC5, 8, "PERSON"))

    train_data.extend(build_train_data(film1, 'Title', ExF1, 17, "WORK_OF_ART"))
    train_data.extend(build_train_data(film2, 'Title', ExF2, 8, "WORK_OF_ART"))
    train_data.extend(build_train_data(film3, 'Title', ExF3, 14, "WORK_OF_ART"))
    train_data.extend(build_train_data(film4, 'Title', ExF4, 18, "WORK_OF_ART"))
    train_data.extend(build_train_data(film5, 'Title', ExF5, 13, "WORK_OF_ART"))

    return train_data

# From https://github.com/explosion/spaCy/blob/master/examples/training/train_ner.py
def train_model():
    nlp = spacy.load('en_core_web_lg')
    ner = nlp.get_pipe("ner")

    train_data = get_train_data()

    for _, annotations in train_data:
        for ent in annotations.get("entities"):
            ner.add_label(ent[2])

    other_pipes = [pipe for pipe in nlp.pipe_names if pipe != "ner"]
    with nlp.disable_pipes(*other_pipes):  # only train NER
        for itn in range(2):
            shuffle(train_data)
            losses = {}
            # batch up the examples using spaCy's minibatch
            batches = minibatch(train_data, size=compounding(4.0, 32.0, 1.001))
            for batch in batches:
                texts, annotations = zip(*batch)
                nlp.update(
                    texts,  # batch of texts
                    annotations,  # batch of annotations
                    drop=0.5,  # dropout - make it harder to memorise data
                    losses=losses,
                )
            print("Losses", losses)

    # test the trained model
    # for text, _ in train_data:
    #     doc = nlp(text)
    #     print("Entities", [(ent.text, ent.label_) for ent in doc.ents])
    #     print("Tokens", [(t.text, t.ent_type_, t.ent_iob) for t in doc])

    output_dir = Path("C:/dev/projects/University/FYP")
    nlp.to_disk(output_dir)
    print("Saved model to", output_dir)

        # # test the saved model
        # print("Loading from", output_dir)
        # nlp2 = spacy.load(output_dir)
        # for text, _ in train_data:
        #     doc = nlp2(text)
        #     print("Entities", [(ent.text, ent.label_) for ent in doc.ents])
        #     print("Tokens", [(t.text, t.ent_type_, t.ent_iob) for t in doc])

if __name__ == "__main__":
    train_model()