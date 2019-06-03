# eind-project
Nieuw Django format maken.
Bijhouden van Data voor een hotel.
Tabel1 waar alle kamers gedefinieerd zijn.
Details Tabel1:
Kamernummer;
hoeveelheid personen;
Vrije kamer?;
Prijs;

Tabel2 maken voor het bijhouden wie er in welke kamer zit.
Details Tabel2:
ID;
Naam;
Wachtwoord;
Kamernummer;

3 bezoekers kunnen gescheiden worden door Tabel2:
1) Staff: geen kamernummer, maar is staff;
2) iemand in het hotel: wel kamernummer en geen staff;
3) iemand die niet in het hotel is: geen kamernummer en geen staff.

Er komt een pagina waar je je mening kan geven. Je kan je mening zowel annoniem, als met je naam erbij neerzetten. Ook het kamernummer komt erbij, zodat daar naar gekeken kan worden als er bijvoorbeeld meerdere slechte feedbacks komen vanuit dezelfde kamer. Tabel3 is meningen tabel, deze wordt met socket.io aangedreven. Cijfer kan aangegeven worden door sterren aan te klikken en er kan een mening getyped worden. dit is niet meer te zien als deze persoon al een review heeft geplaatst. Dan zijn alleen alle reviews te zien. Staff en Persoon3 kunnen ook alleen de reviwes zien. Staff is de enige die het kamernummer erbij ziet.
Details Tabel3:
Naam;
kamernummer;
cijfer;
mening;

Online chat maken met socket.io, waar mensen met elkaar kunnen praten en staff berichten kunnen clippen. Persoon3 kan hier niet bij.
