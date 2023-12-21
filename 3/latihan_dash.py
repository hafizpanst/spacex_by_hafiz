import pandas as pd

def get_dataset():
    df = pd.read_csv("https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBM-DS0321EN-SkillsNetwork/datasets/spacex_launch_dash.csv")
    return df


def main():
    df = get_dataset()
    df.to_csv("")

if __name__ == "__main__":
    main()