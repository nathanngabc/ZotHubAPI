import numpy as np
from gensim.models import KeyedVectors
from sklearn.metrics.pairwise import cosine_similarity

tags = ['Academic', 'Art', 'Athletics', 'Band', 'Book', 'Chess', 'Chorus', 'Community', 'Competition',
        'Computer', 'Dance', 'Debate', 'Drama', 'Educational', 'Engineering', 'Ensemble', 'Environmental',
        'Fitness', 'Foreign', 'Games', 'Gardening', 'History', 'Journalism', 'Language', 'Leadership', 'Literary',
        'Math', 'Music', 'Photography', 'Poetry', 'Politics', 'Science', 'Scouting', 'Service', 'Shakespeare', 'Social',
        'Speech', 'Sports', 'STEM', 'Student', 'Technology', 'Theater', 'Tourism', 'Tradition', 'Travel', 'Volunteering',
        'Wellness', 'Writing', 'Games', 'Magic', 'Food', 'Formal', 'Dinner', 'Lunch', 'Presentation']

wordVectors = np.zeros((len(tags), len(tags))).astype(float)
path = "./GoogleNews-vectors-negative300.bin.gz"
model = KeyedVectors.load_word2vec_format(path, binary=True)
for t in range(len(tags)):
    tags[t] = model[t]
for i in range(len(tags)):
    for j in range(len(tags)):
        if wordVectors[i][j] == 0:
            wordVectors[i][j] = cosine_similarity([tags[i]], [tags[j]])
            wordVectors[j][i] = wordVectors[i][j]

with open('prebuiltModelTagsSimilarity.npy', 'wb') as f:
    np.save(f, wordVectors)

