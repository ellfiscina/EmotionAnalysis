import matplotlib.pyplot as plt

class LexicalDispersion:
  def plot_dis(self, tokens, WORD):
    x=list()
    for i in range(0,len(tokens)):
        if tokens[i] == WORD:
            x.append(i)

    fig, ax = plt.subplots()
    ax.vlines(x, 0, 1, edgecolor="red")
    ax.set_xlim([0, len(tokens)])
    ax.set_xticks([0],minor=True)
    ax.set_ylabel(WORD)
    ax.set_yticks([])
    fig.set_figheight(1)
    return fig
