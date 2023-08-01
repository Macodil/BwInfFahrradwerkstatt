import matplotlib.pyplot as plt
import math
import time as t

start = t.time()  # Zeitmessung
auftreage, nextAuftreage, yAxis = [], [], []  # Liste der Aufträge, Warteliste, -
time = 0
maxAuf = 1  # Index des nächsten zur Warteliste hinzuzufügenden Auftrags


def recountNextTimeFinish():
    duration = auftreage[nextAuftreage[0]][1] - (1020 - (time % 1440))  # Dauer des Auftrags minus was am selben Tag erledigt werden kann
    days = duration // (1020 - 540)  # Ganze benötigte Tage für die Beendung des Auftrags nach dem aktuellen Tag
    lastDay = duration - days * (1020 - 540)  # Benötigte Zeit am letzten Tag
    nextTimeFinish = time + (1440 - time % 1440) + days * 1440 + 540 + lastDay  # Die jetzige Zeit plus alle naderen Berechnungen
    return nextTimeFinish


def getAvgAndMax(filename, shortestFirst, smartSort):
    global time, maxAuf, auftreage, nextAuftreage
    auftreage, nextAuftreage = [], []
    maxAuf = 1
    # Liest die Datei aus und schreibt sie in eine Liste
    with open(filename, 'r', encoding='utf-8') as file:
        lines = filter(None, (line.rstrip() for line in file))
        for line in lines:
            auftreage.append([int(line.split()[0]), int(line.split()[1]), -1])
    # # # # # # # # # # # # # # #
    time = auftreage[0][0]
    nextAuftreage.append(0)
    nextTimeNew = auftreage[1][0]  # Nächste Zeit, wenn ein neuer Auftrag der Warteliste hinzugefügt werden würde
    nextTimeFinish = recountNextTimeFinish()  # Nächste Zeit, wenn der aktuell bearbeitete Auftrag abgeschlossen wäre
    while (True):
        if (maxAuf >= len(auftreage) and len(nextAuftreage) == 0):  # Bricht ab wenn alle Aufräge angenommen und ausgeführt wurden
            break
        # Fügt neuen Auftrag zur Warteliste hinzu
        if (nextTimeNew < nextTimeFinish):
            nextAuftreage.append(maxAuf)
            maxAuf += 1
            if len(nextAuftreage) == 1:
                time = nextTimeNew
                nextTimeFinish = recountNextTimeFinish()
            if maxAuf != len(auftreage):
                nextTimeNew = auftreage[maxAuf][0]
            else:
                nextTimeNew = math.inf
        # # # # # # # # # # # # # #
        # Entfernt Auftrag von Warteliste weil fertig und wählt den als nächstes zu bearbeitenden Auftrag
        else:
            time = nextTimeFinish
            auftreage[nextAuftreage[0]][2] = time
            nextAuftreage.pop(0)
            if smartSort:
                for a in range(len(nextAuftreage)):
                    if (auftreage[nextAuftreage[a]][1] + (time % 1440) <= 1020):
                        nextAuftreage.insert(0, nextAuftreage.pop(a))
                        break
            elif shortestFirst:
                nextAuftreage.sort(key=lambda x: auftreage[x][1])
            if len(nextAuftreage):
                nextTimeFinish = recountNextTimeFinish()
            else:
                nextTimeFinish = math.inf
        # # # # # # # # # # # # # #
    times = [a[2] - a[0] for a in auftreage]  # Rechnet Wartezeit der einzelnen Aufträge aus
    return [round(sum(times) / len(times), 2), max(times)]  # Gibt durchschnittliche und maximale Wartezeit zurück


def showTables(yAxis):  # Erzeugt Graphen
    yAxisFinal = [round(x / 1440, 2) for y in yAxis for x in y]
    yAxisMax = [round(x[1] / 1440, 2) for x in yAxis]
    yAxisAverage = [round(x[0] / 1440, 2) for x in yAxis]
    xAxis = [1, 1.2, 2, 2.2, 3, 3.2, 5, 5.2, 6, 6.2, 7, 7.2, 9, 9.2, 10, 10.2, 11, 11.2, 13, 13.2, 14, 14.2, 15, 15.2, 17, 17.2, 18, 18.2, 19, 19.2]
    tick_label = ["0|1", "", "0|2", "", "0|3", "", "1|1", "", "1|2", "", "1|3", "", "2|1", "", "2|2", "", "2|3", "", "3|1", "", "3|2", "", "3|3", "", "4|1", "", "4|2", "", "4|3", ""]
    plt.bar(xAxis, yAxisFinal, tick_label=tick_label, width=0.2, color=['red', 'red', 'orange', 'orange', 'green', 'green'])
    plt.show()
    xAxis = [1, 2, 3, 5, 6, 7, 9, 10, 11, 13, 14, 15, 17, 18, 19]
    tick_label = ["0|1", "0|2", "0|3", "1|1", "1|2", "1|3", "2|1", "2|2", "2|3", "3|1", "3|2", "3|3", "4|1", "4|2", "4|3"]
    plt.bar(xAxis, yAxisMax, tick_label=tick_label, width=0.5, color=['red', 'orange', 'green'])
    plt.show()
    plt.bar(xAxis, yAxisAverage, tick_label=tick_label, width=0.5, color=['red', 'orange', 'green'])
    plt.show()


if __name__ == "__main__":  # Ruft die Funktion getAvgAndMax für jede zu bearbeitende Datei mit jeder Methode auf
    for x in range(5):
        myFileName = "Fahrradwerkstatt" + str(x) + ".txt"
        yAxis.append(getAvgAndMax(myFileName, False, False))
        yAxis.append(getAvgAndMax(myFileName, True, False))
        yAxis.append(getAvgAndMax(myFileName, False, True))
    print("time:", t.time() - start)
    print(yAxis)
    showTables(yAxis)