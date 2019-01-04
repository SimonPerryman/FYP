def main():
    # # from conversations import conversation_handler

    # # print(conversation_handler.filler())

    # abc = ["1"]

    # if len(abc) == 2 and abc[1] == "Comedy":
    #     print("Yes")
    # else:
    #     print("No")

    namebasics = r'D:\dev\Dataset\name.basics.tsv\data.tsv'
    principals = r'D:\dev\Dataset\title.principals.tsv\data.tsv'
    titleakas = r'D:\dev\Dataset\title.akas.tsv\data.tsv'
    titlebasics = r'D:\dev\Dataset\title.basics.tsv\data.tsv'
    titlecrew = r'D:\dev\Dataset\title.crew.tsv\data.tsv'
    titleratings = r'D:\dev\Dataset\title.ratings.tsv\data.tsv'

    # import csv

    # def writer(file, nameToWrite):
    #     i = 0
    #     fileToWrite = open("Data.txt", "a", encoding="utf8")
    #     fileToWrite.write(nameToWrite)
    #     fileToWrite.write("\n")
    #     with open(file, 'r', encoding="utf8") as tsv:
    #         for line in tsv:
    #             if i < 3:
    #                 fileToWrite.write(line)
    #                 fileToWrite.write("\n")
    #                 i += 1

    #     fileToWrite.write("\n")
    #     fileToWrite.close()

    # writer(namebasics, "namebasics")
    # writer(titleakas, "titleakas")
    # writer(titlebasics, "titlebasics")
    # writer(titlecrew, "titlecrew")
    # writer(titleratings, "titleratings")
    
    # with open(titlebasics, 'r', encoding="utf8") as file:
    #     for line in file:
    #         formatted = line.strip().split('\t')
    #         if formatted[5] is not None or formatted[6] is not None:
    #             print(formatted)
    types = []
    roles = []
    r2 = []
    # att = []
    from collections import Counter
    # with open(namebasics, 'r', encoding="utf8") as file7:
    #     for line in file7:
    #         formatted = line.strip().split('\t')
    #         formatted[4] = formatted[4].split(',')
    #         roles.extend(formatted[4])
    i=0
    l = ""
    with open(titlebasics, 'r', encoding="utf8") as file2:
        for line in file2:
            formatted = line.strip().split('\t')
            if formatted[1] == "movie":
                if i < len(formatted[2]):
                    i = len(formatted[2])
                    l = formatted
            # print(type(formatted[7]))
            # print(type(formatted[4]))
            # formatted[8] = formatted[8].split(",")
            # for genre in formatted[8]:
            #     if genre == "\\N": 
            #         if i < 20:
            #             print(formatted)
            #             i += 1
            # if formatted[4] != r"\\N":
    #             types.append(formatted[4])
    print(i)
    print(l)
    # print(Counter(types))
            # if formatted[3] == 'archive_footage' or formatted[3] == "archive_sound" or formatted[3] == "category":
            # if formatted[3] == r"\\N" or formatted[3] == r"\N":
            #     if i < 5:
            #         print(formatted)
            #         i += 1
            # if formatted[2] == "nm0000001":
            #     print(formatted)
        #     r2.append(formatted[3]) self

    # roles = set(roles)
    # r2 = set(r2)

    # print("[f for f in roles if f not in r2]")
    # print([f for f in roles if f not in r2])
    # print("[f for f in r2 if f not in roles]")
    # print([f for f in r2 if f not in roles])
                

    # print(set(types))
            # if formatted[4] != "\\N":
            #     print("lan", formatted[4])
            # if formatted[3] != "\\N":
            #     print("reg", formatted[3])
    #             types.append(formatted[5])
    #         if formatted[6] != "\\N":
    #             att.append(formatted[6])
    # print(set(types))
    # print(set(att))
    # print("--")
    # tt0016602
    # with open(titlecrew, 'r', encoding="utf8") as file:
    #     for line in file:
    #         formatted = line.strip().split('\t')
    #         if formatted[2] != r"\N":
    #             print(formatted)
    # roles = []
    # from collections import Counter
    # with open(namebasics, 'r', encoding="utf8") as file:
    #     for line in file:
    #         formatted = line.strip().split('\t')
    #         if formatted[4] is not None:
    #             arr = formatted[4].split(",")
    #             if "primaryProfession" in arr:
    #                 print(formatted)
                # roles.extend(formatted[4].split(","))

    # print(Counter(roles))
    # print(set(roles))

    # with open("roles.txt", "w", encoding="utf8") as f2:
    #     f2.write(str(set(roles)))

        

    # import csv
    # from collections import Counter
    # genres = []
    # typea = []
    # with open(r'D:\dev\Dataset\title.basics.tsv\data.tsv','r', encoding="utf8") as tsv:
    #     for line in tsv:
    #         formatted = line.strip().split('\t')
    #         if formatted[1] == "movie":
    #             formatted[2] = formatted[2].lower()
    #             if formatted[2].find("spiderman") != -1:
    #                 print("spiderman", formatted[2])
    #             if formatted[2].find("spider-man") != -1:
    #                 print("spiderman", formatted[2])
    #             # if formatted[2].find("batman") != -1:
    #             #     print("batman", formatted[2])
    #             # if formatted[2].find("superman") != -1:
    #             #     print("sup", formatted[2])
    #             # if formatted[2].find("marvel") != -1:
    #             #     print("marv", formatted[2])
    #             if formatted[2].find("x men") != -1:
    #                 print("xme", formatted[2])
    #             if formatted[2].find("x-men") != -1:
    #                 print("x-me", formatted[2])
    #             if formatted[2].find("venom") != -1:
    #                 print("ve", formatted[2])
    #             if formatted[2].find("deadpool") != -1:
    #                 print("ve", formatted[2])
                    #batman, superman, maybe marvel with some tweaks
            # if not formatted[1].startswith("tv") and not formatted[1] == "video" and not formatted[1] == "videoGame":
            # if formatted[1] == "movie":
            # genrePerFilm = formatted[8].split(",")
            # if "Superhero" in genrePerFilm:
            #     print(formatted)
            # if "Reality-TV" in genrePerFilm:
            #     print("Reality-TV", formatted[2], "type", formatted[1])
            # if "Talk-Show" in genrePerFilm:
            #     print("Talk-Show", formatted[2], "type", formatted[1])
            # if "Game-Show" in genrePerFilm:
            #     print("Game-Show", formatted[2], "type", formatted[1])
            # typea.append(formatted[1])
            # genres.extend(genrePerFilm)

    # genres = set(genres)
                
    # print(Counter(genres))
    # print(Counter(typea))

    # with open("genres.txt", "w") as fa:
    #     fa.write(str(Counter(genres)))

    set1 = [
        "Action",
        "Adult",
        "Adventure",
        "Animation",
    "Biography",
    "Comedy",
    "Crime"	,
    "Documentary",
    "Drama",
    "Family",
    "Fantasy",
    "Film-Noir",
    "Game-Show",
    "History"	,
    "Horror",
    "Music",
    "Musical",
    "Mystery",
    "Romance",
    "Sci-Fi",	
    "Short",
    "Sport",
    "Superhero",
    "Talk-Show"
    "Thriller",
    "War",
    "Western"]

    # print("In given data set but not in imdb site:")
    # print([f for f in genres if f not in set1])
    # print("Not in given data set:")
    # print([f for f in set1 if f not in genres])

    set2 = [
        'Drama', 
    'Documentary', 
    'Comedy', 
    'Action',
    'Romance', 
    'Thriller',
    'Crime', 
    'Horror',
    'Adventure', 
    'Family', 
    'Biography', 
    'Mystery', 
    'History', 
    'Fantasy', 
    'Sci-Fi', 
    'Music', 
    'Musical', 
    'War', 
    'Adult',
    'Western',
    'Animation', 
    'Sport', 
    'News', 
    'Film-Noir',
    'Reality-TV',
     'Talk-Show', 
     'Short',
     'Game-Show'
    ]

    # print([f for f in set2 if f not in set1])
    # print([f for f in set1 if f not in set2])
    
    # import os
    # print(os.getenv('ALLUSERSPROFILE', ''))
    #     # print(item.keys())


if(__name__ == "__main__"):
    main()