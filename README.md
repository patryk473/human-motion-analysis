# human-motion-analysis

Fundament: (wykonane)
-> jest filmik jak człowiek robi serie przysiadów
(stałe ujęcie, od boku, 2D)
-> obliczamy potrzebne kąty (pochylenie tułowia, kąt biodra, kąt kolana), 
-> dokonuje filtracji szumu
-> otrzymujemy wykresy i dane w tabelce

Rozszerzenie: (wykonane)
-> komputer wykrywa początek i koniec ruchu
(mogę wyciągnąć przysiad z serii i zapisać osobno do analizy jako jeden i tak każdy)
-> liczymy dodatkowo czas zejścia i wstawania

Jakość ruchu:(wykonane)
-> Wyświetlanie wszystkich danych na filmiku, czas zejścia, wstawania też, i od razu w kolorach czerwony/zielony feedback na filmiku
-> Komputer sprawdza na podstawie zdefiniowanych progów czy jest dobrze czy źle I DAJE FEEDBACK NA ŻYWO
-> Porównuje każdy przysiad z serii do wzoru I DAJE FEEDBACK NA KONIEC

Rozszerzenie o czujniki:
Dodajemy dwa czujniki na nodze połączone przewodami z ESP32
-> ESP32 wysyła dane (wykonane)
-> Otrzymujemy dane z kamery, a także z czujników (np. odnośnie stabilności ruchu, drgań)
-> możemy dokonać jeszcze dokładniejszej analizy

Rozszerzenie jakości:
-> Więcej danych odnośnie jakości


1) Na podstawie ruchu, ESP32 przejmuje dane
-> Otrzymujemy feedback na żywo (buzzer, ledy, silniczek wybracyjny) + (przewody, rezystory)


DALSZA PRZYSZŁOŚĆ
3) analiza innych ruchów nie tylko przysiadu