from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser

from utils.prompts import EXPLANATION_TEMPLATE

load_dotenv()

llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    google_api_key=st.secrets["GOOGLE_API_KEY"],
    temperature=0.3
)

prompt = PromptTemplate(
    template=EXPLANATION_TEMPLATE,
    input_variables=[
        "market_structure",
        "market_reason",
        "bias",
        "rsi",
        "volume",
        "trade_type",
        "entry",
        "stop_loss",
        "target",
        "risk_reward",
        "warnings"
    ]
)

parser = StrOutputParser()

explanation_chain = (
    prompt
    | llm
    | parser
)
