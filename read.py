# %%
from newsplease import NewsPlease

url = "https://www.stephenmorgan.org.uk/peoples-views-on-how-to-build/"

article = NewsPlease.from_url(url)

article.title

# %%
article.maintext
