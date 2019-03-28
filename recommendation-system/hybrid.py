from collaborative import collaborative_recommender
from content import content_recommender

def hybrid_recommender(userId, filmID):
    content_result = content_recommender(filmID)
    # print(content_result[:5])
    collaborative_result = collaborative_recommender(userId)
    print(len(collaborative_recommender))
    # print(collaborative_result[:5])

    # for film in collaborative_result[:5]:
    #     print(film[1])
    #     print(type(film[1]))
    #     # if film[1] in content_result['FilmID']:
    #     #     print(film[1])

    # a = content_result['FilmID']
    # for v in a:
    #     print(v)
    # print(content_result['FilmID'].values[0], type(content_result['FilmID'].values[0]))
    # print(collaborative_result[0][1], type(collaborative_result[0][1]))

    for i in range(len(collaborative_result)):
        if collaborative_result[i][1] == 'tt0005078':
            print(i)
    # collab = [film for film in collaborative_result if film[1] in content_result['FilmID'].values]
    # print(collab)
    # hybrid_result = [film]
    # content_result['FilmID']
    # print(collaborative_result[1][1])
    # collaborative_result[1]
    print("True")


if __name__ == '__main__':
    hybrid_recommender(629604219, "tt0002130")