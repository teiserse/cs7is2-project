import pycross

class q_learning_agent():
    def __init__(self, picross):
        self.picross = picross
        self.q_table = {}

    def test(self, index, row=True):
        result = self.picross.get_possible_actions(index, row)
        return result

if __name__ == '__main__':
    picross = pycross.from_json(open("pycross/example.json")).read()
    agent = q_learning_agent(picross)
    result = agent.test(1, True)
    print('h')