import warnings
import locale
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
import matplotlib.cbook
matplotlib.use('Agg')

warnings.filterwarnings("ignore", category=matplotlib.cbook.mplDeprecation)

locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')

def setDataModel(dataraw):
    data = {}
    weights = [w for w,_ in dataraw]
    label = [l for _,l in dataraw]
    data['weights'] = weights
    data['label'] = label
    data['items'] = list(range(len(weights)))
    data['bins'] = list(range(300))
    data['bin_capacity'] = 5800
    return data


def solveLinearCut2(data):
    res = {}
    ignore = []
    while len(data['items']) != len(ignore):
        for j in data['bins']:
            if len(data['items']) == len(ignore):
                break
            res[j] = {}
            res[j]['morceau'] = []
            res[j]['used'] = 0
            res[j]['chute'] = 0
            res[j]['mo'] = []
            for i in data['items']:
                if i not in ignore:
                    if res[j]['used'] + data['weights'][i] + 30 < data['bin_capacity']:
                        res[j]['morceau'].append((data['weights'][i], data['label'][i]))
                        res[j]['used'] += data['weights'][i] + 30
                        res[j]['chute'] = data['bin_capacity'] - res[j]['used']
                        ignore.append(i)
    return res

def afficheSol(res):
    if len(res) > 0:
        with PdfPages('Impression.pdf') as pdf:
            # A4 canvas
            fig_width_cm = 21
            fig_height_cm = 9.5
            inches_per_cm = 1 / 2.54
            fig_width = fig_width_cm * inches_per_cm
            fig_height = fig_height_cm * inches_per_cm
            fig_size = [fig_width, fig_height]

            for i in res:
                fig = plt.figure()
                fig.set_size_inches(fig_size)
                fig.patch.set_facecolor('#FFFFFF')
                ax = fig.add_subplot()
                ax.invert_yaxis()
                ax.xaxis.set_visible(False)
                ax.yaxis.set_visible(False)
                ax.set_xlim(0, 5800)
                ax.set_ylim(0, 3)
                ax.set_facecolor('#FFFFFF')
                t = 1
                start = 0
                ax.barh(str(t), 5800, left=start, height=0.5, Fill=None, hatch='///')
                for j in res[i]['morceau']:
                    ax.barh(str(t), j[0], left=start, height=0.5, label=str(j[0]) + ' : ' + j[1])
                    ax.text(start + (j[0] / 2), t - 1, j[0], ha='center', va='bottom',
                            color='#000000')
                    start += j[0]
                    t = 1
                plt.legend(loc='upper left',
                           ncol=1, mode="expand", borderaxespad=0.)
                pdf.savefig(dpi=300, orientation='portarit')
                plt.close()

    print(' | Nombre de barres utilise:', len(res))

if __name__ == '__main__':
    test = [(3000,'01'),(2500,'02'),(1200,'03'),(1500,'04'),(2100,'05'),(3200,'06'),(1000,'07'),(900,'08'),(1400,'09')]
    data = setDataModel(test)
    res = solveLinearCut2(data)
    afficheSol(res)
