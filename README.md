# eind-project

Nieuw Django format maken.
Bijhouden van Data voor een hotel.
Tabel1 waar alle kamers gedefinieerd zijn.

Details Tabel1:

1. Kamernummer;
2. Aantal personen;
3. Prijs;

Tabel2 heeft alle kamers in zich met de data waar ze bezet zijn.

Details Tabel2:

1. Kamernummer;
2. Start Datum;
3. Eind Datum;

Als de lijst weergeven wordt, kun je die sorteren op max prijs, datum en aantal personen die er in die kamer kunnen.

Als er op een kamer gedrukt wordt, worden alle data weergeven wanneer deze kamer nog beschikbaar is. Er kan een request gestuurd worden om de kamer te huren. Ook wordt hierbij neergezet hoe laat iemand waarschijnlijk aankomt.

Tabel3 maken voor het bijhouden wie er welke kamer heeft gehuurd.

Details Tabel3:

1. ID;
2. Naam;
3. Wachtwoord;
4. Kamernummer;

Aan de hand van Tabel3 kunnen alle bezoekers van de site opgedeeld worden in 3 groepen:

| Groep         | kamernummer     | staff?        |
|:------------- |:---------------:| -------------:|
| 1.            | Null            |          True |
| 2.            | not Null        |         False |
| 3.            | Null            |         False |

Er komt een pagina waar je je mening kan geven. Je kan je mening zowel annoniem, als met je naam erbij neerzetten. Ook het kamernummer komt erbij, zodat daar naar gekeken kan worden als er bijvoorbeeld meerdere slechte feedbacks komen vanuit dezelfde kamer. Tabel4 is meningen tabel. Cijfer kunnen aangegeven worden door sterren aan te klikken en er kan een mening getyped worden. dit is niet meer te zien als deze persoon al een review heeft geplaatst. Dan zijn alleen alle reviews te zien. Staff en groep kunnen ook alleen de reviwes zien. Staff is de enige die het kamernummer erbij ziet.

Details Tabel4:

1. Naam;
2. kamernummer;
3. cijfer;
4. mening;

Tabel5 is waar roomcleaning voorbij komt. hier kun je een datum voor prikken wanneer jij er niet bent. Als ze niks opgeven voor een aantal dagen moet daar naar gevraagd worden en moet er dus een melding komen als er een kamer is waar wel mensen zijn, maar geen schoonmaak momenten.

Details Tabel5:

1. Kamernunmmer;
2. datum;
3. tijd;

Online chat maken met socket.io, waar mensen met elkaar kunnen praten en staff berichten kunnen clippen. Persoon3 kan hier niet bij.

![Alt Image Text](htmls.png "Optional Title")
