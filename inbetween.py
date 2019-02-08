import numpy as np
from pathlib import Path
import csv
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import GaussianNB
import matplotlib.pyplot as plt
from sklearn import metrics

def create_card_deck():
    card_values = np.repeat(np.arange(1, 14), 4)
    card_suites = np.tile(np.arange(1, 5), 13)
    deck = np.column_stack([card_suites, card_values])
    deck = deck.reshape((52, 2))
    return deck


def serve_card(deck):
    np.random.shuffle(deck)
    served_card = deck[:2]
    deck = np.delete(deck, [0, 1], axis=0)
    return served_card, deck


def check_cards(first_card, second_card, pick):
    if first_card < pick < second_card:
        return 1
    return 0


def save_result(first_card, second_card, result):
    my_file = Path("in_between.csv")
    if my_file.is_file():
        with open('in_between.csv', mode='a') as datafile:
            data_writer = csv.writer(datafile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)

            data_writer.writerow([first_card, second_card, result])

    else:
        with open('in_between.csv', mode='w') as datafile:
            data_writer = csv.writer(datafile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)

            data_writer.writerow(['first_card', 'second_card', 'result'])
            data_writer.writerow([first_card, second_card, result])


def lets_look_deep():
    df = pd.read_csv("in_between.csv")

    feature_col_names = ['first_card', 'second_card']
    predicted_class_names = ['result']

    x = df[feature_col_names].values
    y = df[predicted_class_names].values
    split_test_size = 0.30

    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=split_test_size, random_state=42)

    # nb_model = GaussianNB()
    # nb_model.fit(x_train, y_train.ravel())

    rf_model = RandomForestClassifier(random_state=42)  # Create random forest object
    rf_model.fit(x_train, y_train.ravel())

    check_this = np.array([[1, 16]])

    nb_predict_test = rf_model.predict(check_this)

    # print(y_test)
    print("Accuracy: {0:.4f}".format(metrics.accuracy_score([[1]], nb_predict_test)))

    return '50%'


def plot_n_see():
    df = pd.read_csv("./in_between.csv")
    positive_df = df.loc[df['result'] == 1]
    negative_df = df.loc[df['result'] == 0]
    ax = positive_df.plot.scatter(x='first_card', y='second_card', color='DarkGreen', label='Group 1')
    negative_df.plot.scatter(x='first_card', y='second_card', color='DarkRed', label='Group 2', ax=ax)
    # plt.isinteractive()
    plt.show()


def play_game():
    quit_me = 1
    # while quit_me:
    for i in range(1000):
        print('\n********************* START ***********************\n')
        deck = create_card_deck()
        served_cards, deck = serve_card(deck)

        cards = served_cards[:, 1]

        first_card = np.amin(cards)
        second_card = np.amax(cards)

        print('First Card:', first_card, '?_?', second_card, 'Second Card')
        # choice = int(input('Enter 1: Pick | 2: Ask Computer | 3: Quit Game\t'))
        choice = 1
        if choice == 1:
            pick = deck[:1][:, 1]
            deck = np.delete(deck, 0, axis=0)
            result = check_cards(first_card, second_card, pick)
            save_result(first_card, second_card, result)
            if result:
                print(pick, '** Won **')
            else:
                print(pick, '** Loose **')
        elif choice == 2:
            prediction = lets_look_deep()
            print('Computer: ', prediction)
        else:
            quit_me = 0
            print('\n=====***** Quit *****=====')
            print('Thanks for playing!!')


if __name__ == "__main__":
    # play_game()
    # lets_look_deep()
    plot_n_see()
