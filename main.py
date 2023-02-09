from gpt import *
from read_data import *
import re
from flask import Flask, render_template

ai.api_key ="/"
df = pd.read_excel('data_hackaton.xlsx')


prompt_ad1 = create_prompt(df, 0)
prompt_ad2 = create_prompt(df, 1)

app = Flask(__name__)
@app.route('/',)
def main():
    return render_template('index.html')

@app.route("/ad_1",)
def prompt1():
    full_filename = os.path.join('static/ad1.jpg')
    return render_template("ad.html", user_image=full_filename)

@app.route("/ad_2")
def prompt2():
    full_filename = os.path.join('static/ad2.jpg')
    return render_template("ad.html", user_image=full_filename)


## To not run GPT too much i save and re open
path_result1= "resultgpt_1.txt"
check_file = os.path.isfile(path_result1)
if check_file:
    with open(path_result1) as f:
        result1 = f.readlines()
else:
    result1 = generate_gpt3_response(prompt_ad1, print_output=True)
    with open("resultgpt_1.txt", "w") as f:
        f.write(result1)

path_result2= "resultgpt_2.txt"
check_file_2 = os.path.isfile(path_result2)
if check_file_2:
    with open(path_result2) as f:
        result2 = f.readlines()
else:
    result2 = generate_gpt3_response(prompt_ad2, print_output=True)
    with open("resultgpt_2.txt", "w") as f:
        f.write(result2)

result1_text = "\n".join(result1)

result2_text = "\n".join(result2)
@app.route("/results")
def result1_app():
    return render_template("results.html", result1=result1_text, result2=result2_text)


# Compare score :
result1 = ' '.join(result1)
score_1 = float(re.findall(r"\d+\.\d+",result1)[0])
result2 =  ' '.join(result2)
score_2 = float(re.findall(r"\d+\.\d+",result2)[0])

# if score_1 - score_2 > 0:
#     print(" Ad 1 is serving better the website than Ad 2 ")
# else:
#     print(" Ad 2 is serving better the website than Ad 1 ")
@app.route("/results/score")
def resultscoreapp():
    return render_template("results2.html", score_1=str(score_1), score_2=str(score_2))


if __name__ == '__main__':
    app.run(debug=True)
