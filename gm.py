import streamlit as st
import pickle
import pandas as pd


def rec_all_game(game):
    game_idx = sample[sample["name"] == game].index[0]
    distances = similarity[game_idx]
    games_list = sorted(list(enumerate(distances)), reverse=True, key=lambda e: e[1])[1:]

    pf = []
    glist = []
    for i in games_list:
        pf.append(sample.iloc[i[0]]["platform"])
        glist.append(sample.iloc[i[0]]["name"])
    return glist, pf


def rec_game(platform, game):
    game_idx = sample[sample["name"] == game].index[0]
    distances = similarity[game_idx]
    games_list = sorted(list(enumerate(distances)), reverse=True, key=lambda e: e[1])[1:]

    pf = []
    glist = []
    for i in games_list:
        pf.append(sample.iloc[i[0]]["platform"])
        glist.append(sample.iloc[i[0]]["name"])

    pf_games = [j for j, k in zip(glist, pf) if k == platform][:21]
    return pf_games


sample = pd.read_csv("1000_games_sample.csv")
data = pickle.load(open("sample_dict.pkl", "rb"))
df = pd.DataFrame(data)
similarity = pickle.load(open("similarity.pkl", "rb"))

st.title("Video Games Recommendation")

gm = st.selectbox("Select Video Game", options = ["Select a Video Game"] + sorted(list(sample["name"])))

plt= st.selectbox("Select Platform", options = ["ALL"] + sorted(list(sample["platform"].unique())))

try:
    if st.button("Recommend Games", use_container_width = True):
        if plt == "ALL":
            final_games_list, final_pf  = rec_all_game(gm)

            gp = {"Game" : final_games_list[: 21], "Platform" : final_pf[: 21]}
            final_df = pd.DataFrame(gp)
            final_df.index = final_df.index + 1

            st.table(final_df)
        else:
            final_games_list = rec_game(plt, gm)

            g = {"Game": final_games_list[: 21]}
            final_df = pd.DataFrame(g)
            final_df.index = final_df.index + 1

            st.table(final_df)
except:
    st.error("Please Select a Video Game")
