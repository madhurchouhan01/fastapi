from pydantic import BaseModel

from crewai.flow import Flow, listen, start, router
from digi_ad.crews.digi_crew.digi_crew import  FAQCrew,StandAloneCrew,RouterCrew, BookDemoCrew
from digi_ad.chat_database import get_chat_history, save_message
import uuid
from dotenv import load_dotenv
load_dotenv()

class DigiState(BaseModel):
    creds : dict[str,str] = {
        "name" : "",
        "email": "",
        "session_id": ""
    }
    user_query : str = ""
    query_type : str = ""
    stand_alone_question : str = ""
    chat_history : str = ""
    final_result: dict[str, str] = {
            "result": ""
        }

class DigiFlow(Flow[DigiState]):
    def __init__(self, st_state: DigiState = None):
        super().__init__()
        if st_state:
            self._state = st_state
    @start()
    def stand_alone_question(self):
        self.state.creds["session_id"] = uuid.uuid4().hex
        self.state.chat_history = get_chat_history(self.state.creds["email"])
        result = (
            StandAloneCrew()
            .crew()
            .kickoff(inputs={"user_query": self._state.user_query, "chat_history" : self.state.chat_history})
        )
        self.state.stand_alone_question = result["question"]


    @router(stand_alone_question)
    def intent_classifier(self):

        result = (
            RouterCrew()
            .crew()
            .kickoff(inputs={"user_query": self.state.stand_alone_question, "chat_history" : self.state.chat_history})
        )

        if result['query_type'] == "faq":
            self.state.query_type="faq"
            return "faq"
        
        elif result['query_type'] == "bookdemo":
            self.state.query_type="bookdemo"
            return "bookdemo"
        else:
            self.state.query_type="invalid input"

    @listen("faq")
    def faqs(self):
        result = (
            FAQCrew()
            .crew()
            .kickoff(inputs={"question": self._state.stand_alone_question})
        )
        self._state.final_result["result"] = result.raw
        print(result.raw)
        save_chat = save_message(user_id=self.state.creds["email"], session_id=self.state.creds["session_id"], user_message=self.state.user_query, bot_message=self.state.final_result["result"])       
        print(save_chat)

    @listen("bookdemo")
    def book_demo_call(self):
        result = (
            BookDemoCrew()
            .crew()
            .kickoff(inputs={"question": self._state.stand_alone_question})
        )
        self._state.final_result["result"] = result.raw
        print(result.raw)
        save_chat = save_message(user_id=self.state.creds["email"], session_id=self.state.creds["session_id"], user_message=self.state.user_query, bot_message=self.state.final_result["result"])       
        print(save_chat)

def kickoff():
    Digi_flow = DigiFlow()
    Digi_flow.kickoff()


def plot():
    Digi_flow = DigiFlow()
    Digi_flow.plot()


if __name__ == "__main__":
    kickoff()
