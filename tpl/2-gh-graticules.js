  /* BEGIN generated file from xkcd2js.sh {{{ */
  /*
   * we always apply the 30W rule, so the code would need to be
   * changed, both here and in the CGI, to go further west… but
   * that would not scale either, anyway, plus we calculate all
   * points using CET/CEST, so we don’t do that
   */
  var graticules = [
	["42", "-6", "<a href=\"https://geohashing.site/geohashing/Ponferrada,_Spain\">Ponferrada, Spain</a>"],
	["42", "-5", "<a href=\"https://geohashing.site/geohashing/Le%C3%B3n,_Spain\">León, Spain</a>"],
	["42", "-4", "<a href=\"https://geohashing.site/geohashing/Palencia,_Spain\">Palencia, Spain</a>"],
	["42", "-3", "<a href=\"https://geohashing.site/geohashing/Burgos,_Spain\">Burgos, Spain</a>"],
	["42", "-2", "<a href=\"https://geohashing.site/geohashing/Vitoria-Gasteiz,_Spain\">Vitoria-Gasteiz, Spain</a>"],
	["42", "-1", "<a href=\"https://geohashing.site/geohashing/Pamplona,_Spain\">Pamplona, Spain</a>"],
	["42", "-0", "<a href=\"https://geohashing.site/geohashing/Huesca,_Spain\">Huesca, Spain</a>"],
	["42", "0", "<a href=\"https://geohashing.site/geohashing/Barbastro,_Spain\">Barbastro, Spain</a>"],
	["42", "1", "<a href=\"https://geohashing.site/geohashing/Andorra\">Andorra</a>"],
	["42", "2", "<a href=\"https://geohashing.site/geohashing/Perpignan,_France\">Perpignan, France</a>"],
	["42", "3", "<a href=\"https://geohashing.site/geohashing/Roses,_Spain\">Roses, Spain</a>"],
	["42", "4", "<a href=\"https://geohashing.site/geohashing/Mediterranean_Sea_42,_4\">Mediterranean Sea 42, 4</a>"],
	["42", "5", "<a href=\"https://geohashing.site/geohashing/Mediterranean_Sea_42,_5\">Mediterranean Sea 42, 5</a>"],
	["42", "6", "<a href=\"https://geohashing.site/geohashing/Porquerolles,_France\">Porquerolles, France</a>"],
	["42", "7", "<a href=\"https://geohashing.site/geohashing/Mediterranean_Sea_42,_7\">Mediterranean Sea 42, 7</a>"],
	["42", "8", "<a href=\"https://geohashing.site/geohashing/Calvi,_France\">Calvi, France</a>"],
	["42", "9", "<a href=\"https://geohashing.site/geohashing/Bastia,_France\">Bastia, France</a>"],
	["42", "10", "<a href=\"https://geohashing.site/geohashing/Piombino,_Italy\">Piombino, Italy</a>"],
	["42", "11", "<a href=\"https://geohashing.site/geohashing/Grosseto,_Italy\">Grosseto, Italy</a>"],
	["42", "12", "<a href=\"https://geohashing.site/geohashing/Terni,_Italy\">Terni, Italy</a>"],
	["43", "-6", "<a href=\"https://geohashing.site/geohashing/Vald%C3%A9s,_Spain\">Valdés, Spain</a>"],
	["43", "-5", "<a href=\"https://geohashing.site/geohashing/Gij%C3%B3n,_Spain\">Gijón, Spain</a>"],
	["43", "-4", "<a href=\"https://geohashing.site/geohashing/Torrelavega,_Spain\">Torrelavega, Spain</a>"],
	["43", "-3", "<a href=\"https://geohashing.site/geohashing/Santander,_Spain\">Santander, Spain</a>"],
	["43", "-2", "<a href=\"https://geohashing.site/geohashing/Bilbao,_Spain\">Bilbao, Spain</a>"],
	["43", "-1", "<a href=\"https://geohashing.site/geohashing/Bayonne,_France\">Bayonne, France</a>"],
	["43", "-0", "<a href=\"https://geohashing.site/geohashing/Pau,_France\">Pau, France</a>"],
	["43", "0", "<a href=\"https://geohashing.site/geohashing/Tarbes,_France\">Tarbes, France</a>"],
	["43", "1", "<a href=\"https://geohashing.site/geohashing/Toulouse,_France\">Toulouse, France</a>"],
	["43", "2", "<a href=\"https://geohashing.site/geohashing/Carcassonne,_France\">Carcassonne, France</a>"],
	["43", "3", "<a href=\"https://geohashing.site/geohashing/Montpellier,_France\">Montpellier, France</a>"],
	["43", "4", "<a href=\"https://geohashing.site/geohashing/N%C3%AEmes,_France\">Nîmes, France</a>"],
	["43", "5", "<a href=\"https://geohashing.site/geohashing/Marseille,_France\">Marseille, France</a>"],
	["43", "6", "<a href=\"https://geohashing.site/geohashing/Draguignan,_France\">Draguignan, France</a>"],
	["43", "7", "<a href=\"https://geohashing.site/geohashing/Nice,_France\">Nice, France</a>"],
	["43", "8", "<a href=\"https://geohashing.site/geohashing/Imperia,_Italy\">Imperia, Italy</a>"],
	["43", "9", "<a href=\"https://geohashing.site/geohashing/Capraia,_Italy\">Capraia, Italy</a>"],
	["43", "10", "<a href=\"https://geohashing.site/geohashing/Livorno,_Italy\">Livorno, Italy</a>"],
	["43", "11", "<a href=\"https://geohashing.site/geohashing/Firenze,_Italy\">Firenze, Italy</a>"],
	["43", "12", "<a href=\"https://geohashing.site/geohashing/Perugia,_Italy\">Perugia, Italy</a>"],
	["44", "-6", "<a href=\"https://geohashing.site/geohashing/Bay_of_Biscay_44,_-6\">Bay of Biscay 44, -6</a>"],
	["44", "-5", "<a href=\"https://geohashing.site/geohashing/Bay_of_Biscay_44,_-5\">Bay of Biscay 44, -5</a>"],
	["44", "-4", "<a href=\"https://geohashing.site/geohashing/Bay_of_Biscay_44,_-4\">Bay of Biscay 44, -4</a>"],
	["44", "-3", "<a href=\"https://geohashing.site/geohashing/Bay_of_Biscay_44,_-3\">Bay of Biscay 44, -3</a>"],
	["44", "-2", "<a href=\"https://geohashing.site/geohashing/Bay_of_Biscay_44,_-2\">Bay of Biscay 44, -2</a>"],
	["44", "-1", "<a href=\"https://geohashing.site/geohashing/Arcachon,_France\">Arcachon, France</a>"],
	["44", "-0", "<a href=\"https://geohashing.site/geohashing/Bordeaux,_France\">Bordeaux, France</a>"],
	["44", "0", "<a href=\"https://geohashing.site/geohashing/Bergerac,_France\">Bergerac, France</a>"],
	["44", "1", "<a href=\"https://geohashing.site/geohashing/Montauban,_France\">Montauban, France</a>"],
	["44", "2", "<a href=\"https://geohashing.site/geohashing/Aurillac,_France\">Aurillac, France</a>"],
	["44", "3", "<a href=\"https://geohashing.site/geohashing/Millau,_France\">Millau, France</a>"],
	["44", "4", "<a href=\"https://geohashing.site/geohashing/Valence,_France\">Valence, France</a>"],
	["44", "5", "<a href=\"https://geohashing.site/geohashing/Carpentras,_France\">Carpentras, France</a>"],
	["44", "6", "<a href=\"https://geohashing.site/geohashing/Gap,_France\">Gap, France</a>"],
	["44", "7", "<a href=\"https://geohashing.site/geohashing/Cuneo,_Italy\">Cuneo, Italy</a>"],
	["44", "8", "<a href=\"https://geohashing.site/geohashing/Genova,_Italy\">Genova, Italy</a>"],
	["44", "9", "<a href=\"https://geohashing.site/geohashing/La_Spezia,_Italy\">La Spezia, Italy</a>"],
	["44", "10", "<a href=\"https://geohashing.site/geohashing/Parma,_Italy\">Parma, Italy</a>"],
	["44", "11", "<a href=\"https://geohashing.site/geohashing/Bologna,_Italy\">Bologna, Italy</a>"],
	["44", "12", "<a href=\"https://geohashing.site/geohashing/Ravenna,_Italy\">Ravenna, Italy</a>"],
	["45", "-6", "<a href=\"https://geohashing.site/geohashing/Atlantic_Ocean_45,_-6\">Atlantic Ocean 45, -6</a>"],
	["45", "-5", "<a href=\"https://geohashing.site/geohashing/Bay_of_Biscay_45,_-5\">Bay of Biscay 45, -5</a>"],
	["45", "-4", "<a href=\"https://geohashing.site/geohashing/Bay_of_Biscay_45,_-4\">Bay of Biscay 45, -4</a>"],
	["45", "-3", "<a href=\"https://geohashing.site/geohashing/Bay_of_Biscay_45,_-3\">Bay of Biscay 45, -3</a>"],
	["45", "-2", "<a href=\"https://geohashing.site/geohashing/Bay_of_Biscay_45,_-2\">Bay of Biscay 45, -2</a>"],
	["45", "-1", "<a href=\"https://geohashing.site/geohashing/Royan,_France\">Royan, France</a>"],
	["45", "-0", "<a href=\"https://geohashing.site/geohashing/Saintes,_France\">Saintes, France</a>"],
	["45", "0", "<a href=\"https://geohashing.site/geohashing/Angoul%C3%AAme,_France\">Angoulême, France</a>"],
	["45", "1", "<a href=\"https://geohashing.site/geohashing/Limoges,_France\">Limoges, France</a>"],
	["45", "2", "<a href=\"https://geohashing.site/geohashing/Ussel,_France\">Ussel, France</a>"],
	["45", "3", "<a href=\"https://geohashing.site/geohashing/Clermont-Ferrand,_France\">Clermont-Ferrand, France</a>"],
	["45", "4", "<a href=\"https://geohashing.site/geohashing/Lyon,_France\">Lyon, France</a>"],
	["45", "5", "<a href=\"https://geohashing.site/geohashing/Grenoble,_France\">Grenoble, France</a>"],
	["45", "6", "<a href=\"https://geohashing.site/geohashing/Annecy,_France\">Annecy, France</a>"],
	["45", "7", "<a href=\"https://geohashing.site/geohashing/Torino,_Italy\">Torino, Italy</a>"],
	["45", "8", "<a href=\"https://geohashing.site/geohashing/Novara,_Italy\">Novara, Italy</a>"],
	["45", "9", "<a href=\"https://geohashing.site/geohashing/Milano,_Italy\">Milano, Italy</a>"],
	["45", "10", "<a href=\"https://geohashing.site/geohashing/Verona,_Italy\">Verona, Italy</a>"],
	["45", "11", "<a href=\"https://geohashing.site/geohashing/Padova,_Italy\">Padova, Italy</a>"],
	["45", "12", "<a href=\"https://geohashing.site/geohashing/Venezia,_Italy\">Venezia, Italy</a>"],
	["46", "-6", "<a href=\"https://geohashing.site/geohashing/Atlantic_Ocean_46,_-6\">Atlantic Ocean 46, -6</a>"],
	["46", "-5", "<a href=\"https://geohashing.site/geohashing/Bay_of_Biscay_46,_-5\">Bay of Biscay 46, -5</a>"],
	["46", "-4", "<a href=\"https://geohashing.site/geohashing/Bay_of_Biscay_46,_-4\">Bay of Biscay 46, -4</a>"],
	["46", "-3", "<a href=\"https://geohashing.site/geohashing/Bay_of_Biscay_46,_-3\">Bay of Biscay 46, -3</a>"],
	["46", "-2", "<a href=\"https://geohashing.site/geohashing/L%27%C3%8Ele-d%27Yeu,_France\">L'Île-d'Yeu, France</a>"],
	["46", "-1", "<a href=\"https://geohashing.site/geohashing/La_Roche-sur-Yon,_France\">La Roche-sur-Yon, France</a>"],
	["46", "-0", "<a href=\"https://geohashing.site/geohashing/Niort,_France\">Niort, France</a>"],
	["46", "0", "<a href=\"https://geohashing.site/geohashing/Poitiers,_France\">Poitiers, France</a>"],
	["46", "1", "<a href=\"https://geohashing.site/geohashing/Ch%C3%A2teauroux,_France\">Châteauroux, France</a>"],
	["46", "2", "<a href=\"https://geohashing.site/geohashing/Montlu%C3%A7on,_France\">Montluçon, France</a>"],
	["46", "3", "<a href=\"https://geohashing.site/geohashing/Nevers,_France\">Nevers, France</a>"],
	["46", "4", "<a href=\"https://geohashing.site/geohashing/Chalon-sur-Sa%C3%B4ne,_France\">Chalon-sur-Saône, France</a>"],
	["46", "5", "<a href=\"https://geohashing.site/geohashing/Bourg-en-Bresse,_France\">Bourg-en-Bresse, France</a>"],
	["46", "6", "<a href=\"https://geohashing.site/geohashing/Gen%C3%A8ve,_Switzerland\">Genève, Switzerland</a>"],
	["46", "7", "<a href=\"https://geohashing.site/geohashing/Bern,_Switzerland\">Bern, Switzerland</a>"],
	["46", "8", "<a href=\"https://geohashing.site/geohashing/Lugano,_Switzerland\">Lugano, Switzerland</a>"],
	["46", "9", "<a href=\"https://geohashing.site/geohashing/Chur,_Switzerland\">Chur, Switzerland</a>"],
	["46", "10", "<a href=\"https://geohashing.site/geohashing/Livigno,_Italy\">Livigno, Italy</a>"],
	["46", "11", "<a href=\"https://geohashing.site/geohashing/Trento,_Italy\">Trento, Italy</a>"],
	["46", "12", "<a href=\"https://geohashing.site/geohashing/Belluno,_Italy\">Belluno, Italy</a>"],
	["47", "-6", "<a href=\"https://geohashing.site/geohashing/Atlantic_Ocean_47,_-6\">Atlantic Ocean 47, -6</a>"],
	["47", "-5", "<a href=\"https://geohashing.site/geohashing/Atlantic_Ocean_47,_-5\">Atlantic Ocean 47, -5</a>"],
	["47", "-4", "<a href=\"https://geohashing.site/geohashing/Quimper,_France\">Quimper, France</a>"],
	["47", "-3", "<a href=\"https://geohashing.site/geohashing/Lorient,_France\">Lorient, France</a>"],
	["47", "-2", "<a href=\"https://geohashing.site/geohashing/Vannes,_France\">Vannes, France</a>"],
	["47", "-1", "<a href=\"https://geohashing.site/geohashing/Nantes,_France\">Nantes, France</a>"],
	["47", "-0", "<a href=\"https://geohashing.site/geohashing/Angers,_France\">Angers, France</a>"],
	["47", "0", "<a href=\"https://geohashing.site/geohashing/Tours,_France\">Tours, France</a>"],
	["47", "1", "<a href=\"https://geohashing.site/geohashing/Orl%C3%A9ans,_France\">Orléans, France</a>"],
	["47", "2", "<a href=\"https://geohashing.site/geohashing/Bourges,_France\">Bourges, France</a>"],
	["47", "3", "<a href=\"https://geohashing.site/geohashing/Auxerre,_France\">Auxerre, France</a>"],
	["47", "4", "<a href=\"https://geohashing.site/geohashing/Beaune,_France\">Beaune, France</a>"],
	["47", "5", "<a href=\"https://geohashing.site/geohashing/Dijon,_France\">Dijon, France</a>"],
	["47", "6", "<a href=\"https://geohashing.site/geohashing/Besan%C3%A7on,_France\">Besançon, France</a>"],
	["47", "7", "<a href=\"https://geohashing.site/geohashing/Basel,_Switzerland\">Basel, Switzerland</a>"],
	["47", "8", "<a href=\"https://geohashing.site/geohashing/Z%C3%BCrich,_Switzerland\">Zürich, Switzerland</a>"],
	["47", "9", "<a href=\"https://geohashing.site/geohashing/St._Gallen,_Switzerland\">St. Gallen, Switzerland</a>"],
	["47", "10", "<a href=\"https://geohashing.site/geohashing/Kempten,_Germany\">Kempten, Germany</a>"],
	["47", "11", "<a href=\"https://geohashing.site/geohashing/Innsbruck,_Austria\">Innsbruck, Austria</a>"],
	["47", "12", "<a href=\"https://geohashing.site/geohashing/Rosenheim,_Germany\">Rosenheim, Germany</a>"],
	["48", "-6", "<a href=\"https://geohashing.site/geohashing/Atlantic_Ocean_48,_-6\">Atlantic Ocean 48, -6</a>"],
	["48", "-5", "<a href=\"https://geohashing.site/geohashing/Ouessant,_France\">Ouessant, France</a>"],
	["48", "-4", "<a href=\"https://geohashing.site/geohashing/Brest,_France\">Brest, France</a>"],
	["48", "-3", "<a href=\"https://geohashing.site/geohashing/Lannion,_France\">Lannion, France</a>"],
	["48", "-2", "<a href=\"https://geohashing.site/geohashing/Saint-Brieuc,_France\">Saint-Brieuc, France</a>"],
	["48", "-1", "<a href=\"https://geohashing.site/geohashing/Rennes,_France\">Rennes, France</a>"],
	["48", "-0", "<a href=\"https://geohashing.site/geohashing/Laval,_France\">Laval, France</a>"],
	["48", "0", "<a href=\"https://geohashing.site/geohashing/Le_Mans,_France\">Le Mans, France</a>"],
	["48", "1", "<a href=\"https://geohashing.site/geohashing/Chartres,_France\">Chartres, France</a>"],
	["48", "2", "<a href=\"https://geohashing.site/geohashing/Paris,_France\">Paris, France</a>"],
	["48", "3", "<a href=\"https://geohashing.site/geohashing/Sens,_France\">Sens, France</a>"],
	["48", "4", "<a href=\"https://geohashing.site/geohashing/Troyes,_France\">Troyes, France</a>"],
	["48", "5", "<a href=\"https://geohashing.site/geohashing/Chaumont,_France\">Chaumont, France</a>"],
	["48", "6", "<a href=\"https://geohashing.site/geohashing/Nancy,_France\">Nancy, France</a>"],
	["48", "7", "<a href=\"https://geohashing.site/geohashing/Strasbourg,_France\">Strasbourg, France</a>"],
	["48", "8", "<a href=\"https://geohashing.site/geohashing/Pforzheim,_Germany\">Pforzheim, Germany</a>"],
	["48", "9", "<a href=\"https://geohashing.site/geohashing/Stuttgart,_Germany\">Stuttgart, Germany</a>"],
	["48", "10", "<a href=\"https://geohashing.site/geohashing/Augsburg,_Germany\">Augsburg, Germany</a>"],
	["48", "11", "<a href=\"https://geohashing.site/geohashing/M%C3%BCnchen,_Germany\">München, Germany</a>"],
	["48", "12", "<a href=\"https://geohashing.site/geohashing/Landshut,_Germany\">Landshut, Germany</a>"],
	["49", "-6", "<a href=\"https://geohashing.site/geohashing/Isles_of_Scilly,_United_Kingdom\">Isles of Scilly, United Kingdom</a>"],
	["49", "-5", "<a href=\"https://geohashing.site/geohashing/Lizard_Point,_United_Kingdom\">Lizard Point, United Kingdom</a>"],
	["49", "-4", "<a href=\"https://geohashing.site/geohashing/English_Channel_49,_-4\">English Channel 49, -4</a>"],
	["49", "-3", "<a href=\"https://geohashing.site/geohashing/English_Channel_49,_-3\">English Channel 49, -3</a>"],
	["49", "-2", "<a href=\"https://geohashing.site/geohashing/Channel_Islands\">Channel Islands</a>"],
	["49", "-1", "<a href=\"https://geohashing.site/geohashing/Cherbourg,_France\">Cherbourg, France</a>"],
	["49", "-0", "<a href=\"https://geohashing.site/geohashing/Caen,_France\">Caen, France</a>"],
	["49", "0", "<a href=\"https://geohashing.site/geohashing/Le_Havre,_France\">Le Havre, France</a>"],
	["49", "1", "<a href=\"https://geohashing.site/geohashing/Rouen,_France\">Rouen, France</a>"],
	["49", "2", "<a href=\"https://geohashing.site/geohashing/Amiens,_France\">Amiens, France</a>"],
	["49", "3", "<a href=\"https://geohashing.site/geohashing/Saint-Quentin,_France\">Saint-Quentin, France</a>"],
	["49", "4", "<a href=\"https://geohashing.site/geohashing/Reims,_France\">Reims, France</a>"],
	["49", "5", "<a href=\"https://geohashing.site/geohashing/Verdun,_France\">Verdun, France</a>"],
	["49", "6", "<a href=\"https://geohashing.site/geohashing/Luxembourg,_Luxembourg\">Luxembourg, Luxembourg</a>"],
	["49", "7", "<a href=\"https://geohashing.site/geohashing/Kaiserslautern,_Germany\">Kaiserslautern, Germany</a>"],
	["49", "8", "<a href=\"https://geohashing.site/geohashing/Mannheim,_Germany\">Mannheim, Germany</a>"],
	["49", "9", "<a href=\"https://geohashing.site/geohashing/W%C3%BCrzburg,_Germany\">Würzburg, Germany</a>"],
	["49", "10", "<a href=\"https://geohashing.site/geohashing/Bamberg,_Germany\">Bamberg, Germany</a>"],
	["49", "11", "<a href=\"https://geohashing.site/geohashing/N%C3%BCrnberg,_Germany\">Nürnberg, Germany</a>"],
	["49", "12", "<a href=\"https://geohashing.site/geohashing/Regensburg,_Germany\">Regensburg, Germany</a>"],
	["50", "-6", "<a href=\"https://geohashing.site/geohashing/Atlantic_Ocean_50,_-6\">Atlantic Ocean 50, -6</a>"],
	["50", "-5", "<a href=\"https://geohashing.site/geohashing/Camborne,_United_Kingdom\">Camborne, United Kingdom</a>"],
	["50", "-4", "<a href=\"https://geohashing.site/geohashing/Plymouth,_United_Kingdom\">Plymouth, United Kingdom</a>"],
	["50", "-3", "<a href=\"https://geohashing.site/geohashing/Exeter,_United_Kingdom\">Exeter, United Kingdom</a>"],
	["50", "-2", "<a href=\"https://geohashing.site/geohashing/Weymouth,_United_Kingdom\">Weymouth, United Kingdom</a>"],
	["50", "-1", "<a href=\"https://geohashing.site/geohashing/Southampton,_United_Kingdom\">Southampton, United Kingdom</a>"],
	["50", "-0", "<a href=\"https://geohashing.site/geohashing/Brighton,_United_Kingdom\">Brighton, United Kingdom</a>"],
	["50", "0", "<a href=\"https://geohashing.site/geohashing/Eastbourne,_United_Kingdom\">Eastbourne, United Kingdom</a>"],
	["50", "1", "<a href=\"https://geohashing.site/geohashing/Calais,_France\">Calais, France</a>"],
	["50", "2", "<a href=\"https://geohashing.site/geohashing/Arras,_France\">Arras, France</a>"],
	["50", "3", "<a href=\"https://geohashing.site/geohashing/Lille,_France\">Lille, France</a>"],
	["50", "4", "<a href=\"https://geohashing.site/geohashing/Bruxelles,_Belgium\">Bruxelles, Belgium</a>"],
	["50", "5", "<a href=\"https://geohashing.site/geohashing/Li%C3%A8ge,_Belgium\">Liège, Belgium</a>"],
	["50", "6", "<a href=\"https://geohashing.site/geohashing/K%C3%B6ln,_Germany\">Köln, Germany</a>"],
	["50", "7", "<a href=\"https://geohashing.site/geohashing/Bonn,_Germany\">Bonn, Germany</a>"],
	["50", "8", "<a href=\"https://geohashing.site/geohashing/Frankfurt_am_Main,_Germany\">Frankfurt am Main, Germany</a>"],
	["50", "9", "<a href=\"https://geohashing.site/geohashing/Fulda,_Germany\">Fulda, Germany</a>"],
	["50", "10", "<a href=\"https://geohashing.site/geohashing/Schweinfurt,_Germany\">Schweinfurt, Germany</a>"],
	["50", "11", "<a href=\"https://geohashing.site/geohashing/Erfurt,_Germany\">Erfurt, Germany</a>"],
	["50", "12", "<a href=\"https://geohashing.site/geohashing/Chemnitz,_Germany\">Chemnitz, Germany</a>"],
	["51", "-6", "<a href=\"https://geohashing.site/geohashing/Atlantic_Ocean_51,_-6\">Atlantic Ocean 51, -6</a>"],
	["51", "-5", "<a href=\"https://geohashing.site/geohashing/Milford_Haven,_United_Kingdom\">Milford Haven, United Kingdom</a>"],
	["51", "-4", "<a href=\"https://geohashing.site/geohashing/Barnstaple,_United_Kingdom\">Barnstaple, United Kingdom</a>"],
	["51", "-3", "<a href=\"https://geohashing.site/geohashing/Cardiff,_United_Kingdom\">Cardiff, United Kingdom</a>"],
	["51", "-2", "<a href=\"https://geohashing.site/geohashing/Bristol,_United_Kingdom\">Bristol, United Kingdom</a>"],
	["51", "-1", "<a href=\"https://geohashing.site/geohashing/Swindon,_United_Kingdom\">Swindon, United Kingdom</a>"],
	["51", "-0", "<a href=\"https://geohashing.site/geohashing/London_West,_United_Kingdom\">London West, United Kingdom</a>"],
	["51", "0", "<a href=\"https://geohashing.site/geohashing/London_East,_United_Kingdom\">London East, United Kingdom</a>"],
	["51", "1", "<a href=\"https://geohashing.site/geohashing/Canterbury,_United_Kingdom\">Canterbury, United Kingdom</a>"],
	["51", "2", "<a href=\"https://geohashing.site/geohashing/Dunkerque,_France\">Dunkerque, France</a>"],
	["51", "3", "<a href=\"https://geohashing.site/geohashing/Gent,_Belgium\">Gent, Belgium</a>"],
	["51", "4", "<a href=\"https://geohashing.site/geohashing/Rotterdam,_Netherlands\">Rotterdam, Netherlands</a>"],
	["51", "5", "<a href=\"https://geohashing.site/geohashing/Eindhoven,_Netherlands\">Eindhoven, Netherlands</a>"],
	["51", "6", "<a href=\"https://geohashing.site/geohashing/D%C3%BCsseldorf,_Germany\">Düsseldorf, Germany</a>"],
	["51", "7", "<a href=\"https://geohashing.site/geohashing/Dortmund,_Germany\">Dortmund, Germany</a>"],
	["51", "8", "<a href=\"https://geohashing.site/geohashing/Paderborn,_Germany\">Paderborn, Germany</a>"],
	["51", "9", "<a href=\"https://geohashing.site/geohashing/Kassel,_Germany\">Kassel, Germany</a>"],
	["51", "10", "<a href=\"https://geohashing.site/geohashing/Nordhausen,_Germany\">Nordhausen, Germany</a>"],
	["51", "11", "<a href=\"https://geohashing.site/geohashing/Halle_(Saale),_Germany\">Halle (Saale), Germany</a>"],
	["51", "12", "<a href=\"https://geohashing.site/geohashing/Leipzig,_Germany\">Leipzig, Germany</a>"],
	["52", "-6", "<a href=\"https://geohashing.site/geohashing/Carlow,_Ireland\">Carlow, Ireland</a>"],
	["52", "-5", "<a href=\"https://geohashing.site/geohashing/Fishguard,_United_Kingdom\">Fishguard, United Kingdom</a>"],
	["52", "-4", "<a href=\"https://geohashing.site/geohashing/Aberystwyth,_United_Kingdom\">Aberystwyth, United Kingdom</a>"],
	["52", "-3", "<a href=\"https://geohashing.site/geohashing/Mid_Wales,_United_Kingdom\">Mid Wales, United Kingdom</a>"],
	["52", "-2", "<a href=\"https://geohashing.site/geohashing/Shrewsbury,_United_Kingdom\">Shrewsbury, United Kingdom</a>"],
	["52", "-1", "<a href=\"https://geohashing.site/geohashing/Birmingham,_United_Kingdom\">Birmingham, United Kingdom</a>"],
	["52", "-0", "<a href=\"https://geohashing.site/geohashing/Northampton,_United_Kingdom\">Northampton, United Kingdom</a>"],
	["52", "0", "<a href=\"https://geohashing.site/geohashing/Cambridge,_United_Kingdom\">Cambridge, United Kingdom</a>"],
	["52", "1", "<a href=\"https://geohashing.site/geohashing/Norwich,_United_Kingdom\">Norwich, United Kingdom</a>"],
	["52", "2", "<a href=\"https://geohashing.site/geohashing/North_Sea_52,_2\">North Sea 52, 2</a>"],
	["52", "3", "<a href=\"https://geohashing.site/geohashing/North_Sea_52,_3\">North Sea 52, 3</a>"],
	["52", "4", "<a href=\"https://geohashing.site/geohashing/Amsterdam,_Netherlands\">Amsterdam, Netherlands</a>"],
	["52", "5", "<a href=\"https://geohashing.site/geohashing/Utrecht,_Netherlands\">Utrecht, Netherlands</a>"],
	["52", "6", "<a href=\"https://geohashing.site/geohashing/Enschede,_Netherlands\">Enschede, Netherlands</a>"],
	["52", "7", "<a href=\"https://geohashing.site/geohashing/Rheine,_Germany\">Rheine, Germany</a>"],
	["52", "8", "<a href=\"https://geohashing.site/geohashing/Bielefeld,_Germany\">Bielefeld, Germany</a>"],
	["52", "9", "<a href=\"https://geohashing.site/geohashing/Hannover,_Germany\">Hannover, Germany</a>"],
	["52", "10", "<a href=\"https://geohashing.site/geohashing/Braunschweig,_Germany\">Braunschweig, Germany</a>"],
	["52", "11", "<a href=\"https://geohashing.site/geohashing/Magdeburg,_Germany\">Magdeburg, Germany</a>"],
	["52", "12", "<a href=\"https://geohashing.site/geohashing/Brandenburg,_Germany\">Brandenburg, Germany</a>"],
	["53", "-6", "<a href=\"https://geohashing.site/geohashing/Dublin,_Ireland\">Dublin, Ireland</a>"],
	["53", "-5", "<a href=\"https://geohashing.site/geohashing/Irish_Sea_53,_-5\">Irish Sea 53, -5</a>"],
	["53", "-4", "<a href=\"https://geohashing.site/geohashing/Anglesey,_United_Kingdom\">Anglesey, United Kingdom</a>"],
	["53", "-3", "<a href=\"https://geohashing.site/geohashing/Blackpool,_United_Kingdom\">Blackpool, United Kingdom</a>"],
	["53", "-2", "<a href=\"https://geohashing.site/geohashing/Manchester,_United_Kingdom\">Manchester, United Kingdom</a>"],
	["53", "-1", "<a href=\"https://geohashing.site/geohashing/Sheffield,_United_Kingdom\">Sheffield, United Kingdom</a>"],
	["53", "-0", "<a href=\"https://geohashing.site/geohashing/Hull,_United_Kingdom\">Hull, United Kingdom</a>"],
	["53", "0", "<a href=\"https://geohashing.site/geohashing/Skegness,_United_Kingdom\">Skegness, United Kingdom</a>"],
	["53", "1", "<a href=\"https://geohashing.site/geohashing/North_Sea_53,_1\">North Sea 53, 1</a>"],
	["53", "2", "<a href=\"https://geohashing.site/geohashing/North_Sea_53,_2\">North Sea 53, 2</a>"],
	["53", "3", "<a href=\"https://geohashing.site/geohashing/North_Sea_53,_3\">North Sea 53, 3</a>"],
	["53", "4", "<a href=\"https://geohashing.site/geohashing/Texel,_Netherlands\">Texel, Netherlands</a>"],
	["53", "5", "<a href=\"https://geohashing.site/geohashing/Leeuwarden,_Netherlands\">Leeuwarden, Netherlands</a>"],
	["53", "6", "<a href=\"https://geohashing.site/geohashing/Groningen,_Netherlands\">Groningen, Netherlands</a>"],
	["53", "7", "<a href=\"https://geohashing.site/geohashing/Emden,_Germany\">Emden, Germany</a>"],
	["53", "8", "<a href=\"https://geohashing.site/geohashing/Bremen,_Germany\">Bremen, Germany</a>"],
	["53", "9", "<a href=\"https://geohashing.site/geohashing/Hamburg_(West),_Germany\">Hamburg (West), Germany</a>"],
	["53", "10", "<a href=\"https://geohashing.site/geohashing/Hamburg_(East),_Germany\">Hamburg (East), Germany</a>"],
	["53", "11", "<a href=\"https://geohashing.site/geohashing/Schwerin,_Germany\">Schwerin, Germany</a>"],
	["53", "12", "<a href=\"https://geohashing.site/geohashing/G%C3%BCstrow,_Germany\">Güstrow, Germany</a>"],
	["54", "-6", "<a href=\"https://geohashing.site/geohashing/Lisburn,_United_Kingdom\">Lisburn, United Kingdom</a>"],
	["54", "-5", "<a href=\"https://geohashing.site/geohashing/Belfast,_United_Kingdom\">Belfast, United Kingdom</a>"],
	["54", "-4", "<a href=\"https://geohashing.site/geohashing/Isle_of_Man\">Isle of Man</a>"],
	["54", "-3", "<a href=\"https://geohashing.site/geohashing/Barrow-in-Furness,_United_Kingdom\">Barrow-in-Furness, United Kingdom</a>"],
	["54", "-2", "<a href=\"https://geohashing.site/geohashing/Carlisle,_United_Kingdom\">Carlisle, United Kingdom</a>"],
	["54", "-1", "<a href=\"https://geohashing.site/geohashing/Middlesbrough,_United_Kingdom\">Middlesbrough, United Kingdom</a>"],
	["54", "-0", "<a href=\"https://geohashing.site/geohashing/Scarborough,_United_Kingdom\">Scarborough, United Kingdom</a>"],
	["54", "0", "<a href=\"https://geohashing.site/geohashing/North_Sea_54,_0\">North Sea 54, 0</a>"],
	["54", "1", "<a href=\"https://geohashing.site/geohashing/North_Sea_54,_1\">North Sea 54, 1</a>"],
	["54", "2", "<a href=\"https://geohashing.site/geohashing/North_Sea_54,_2\">North Sea 54, 2</a>"],
	["54", "3", "<a href=\"https://geohashing.site/geohashing/North_Sea_54,_3\">North Sea 54, 3</a>"],
	["54", "4", "<a href=\"https://geohashing.site/geohashing/North_Sea_54,_4\">North Sea 54, 4</a>"],
	["54", "5", "<a href=\"https://geohashing.site/geohashing/North_Sea_54,_5\">North Sea 54, 5</a>"],
	["54", "6", "<a href=\"https://geohashing.site/geohashing/North_Sea_54,_6\">North Sea 54, 6</a>"],
	["54", "7", "<a href=\"https://geohashing.site/geohashing/Helgoland,_Germany\">Helgoland, Germany</a>"],
	["54", "8", "<a href=\"https://geohashing.site/geohashing/T%C3%B8nder,_Denmark\">Tønder, Denmark</a>"],
	["54", "9", "<a href=\"https://geohashing.site/geohashing/Flensburg,_Germany\">Flensburg, Germany</a>"],
	["54", "10", "<a href=\"https://geohashing.site/geohashing/Kiel,_Germany\">Kiel, Germany</a>"],
	["54", "11", "<a href=\"https://geohashing.site/geohashing/Nyk%C3%B8bing_Falster,_Denmark\">Nykøbing Falster, Denmark</a>"],
	["54", "12", "<a href=\"https://geohashing.site/geohashing/Rostock,_Germany\">Rostock, Germany</a>"],
	["55", "-6", "<a href=\"https://geohashing.site/geohashing/Coleraine,_United_Kingdom\">Coleraine, United Kingdom</a>"],
	["55", "-5", "<a href=\"https://geohashing.site/geohashing/Campbeltown,_United_Kingdom\">Campbeltown, United Kingdom</a>"],
	["55", "-4", "<a href=\"https://geohashing.site/geohashing/Glasgow,_United_Kingdom\">Glasgow, United Kingdom</a>"],
	["55", "-3", "<a href=\"https://geohashing.site/geohashing/Edinburgh,_United_Kingdom\">Edinburgh, United Kingdom</a>"],
	["55", "-2", "<a href=\"https://geohashing.site/geohashing/Jedburgh,_United_Kingdom\">Jedburgh, United Kingdom</a>"],
	["55", "-1", "<a href=\"https://geohashing.site/geohashing/Blyth,_United_Kingdom\">Blyth, United Kingdom</a>"],
	["55", "-0", "<a href=\"https://geohashing.site/geohashing/North_Sea_55,_-0\">North Sea 55, -0</a>"],
	["55", "0", "<a href=\"https://geohashing.site/geohashing/North_Sea_55,_0\">North Sea 55, 0</a>"],
	["55", "1", "<a href=\"https://geohashing.site/geohashing/North_Sea_55,_1\">North Sea 55, 1</a>"],
	["55", "2", "<a href=\"https://geohashing.site/geohashing/North_Sea_55,_2\">North Sea 55, 2</a>"],
	["55", "3", "<a href=\"https://geohashing.site/geohashing/North_Sea_55,_3\">North Sea 55, 3</a>"],
	["55", "4", "<a href=\"https://geohashing.site/geohashing/North_Sea_55,_4\">North Sea 55, 4</a>"],
	["55", "5", "<a href=\"https://geohashing.site/geohashing/North_Sea_55,_5\">North Sea 55, 5</a>"],
	["55", "6", "<a href=\"https://geohashing.site/geohashing/North_Sea_55,_6\">North Sea 55, 6</a>"],
	["55", "7", "<a href=\"https://geohashing.site/geohashing/North_Sea_55,_7\">North Sea 55, 7</a>"],
	["55", "8", "<a href=\"https://geohashing.site/geohashing/Esbjerg,_Denmark\">Esbjerg, Denmark</a>"],
	["55", "9", "<a href=\"https://geohashing.site/geohashing/Kolding,_Denmark\">Kolding, Denmark</a>"],
	["55", "10", "<a href=\"https://geohashing.site/geohashing/Odense,_Denmark\">Odense, Denmark</a>"],
	["55", "11", "<a href=\"https://geohashing.site/geohashing/N%C3%A6stved,_Denmark\">Næstved, Denmark</a>"],
	["55", "12", "<a href=\"https://geohashing.site/geohashing/K%C3%B8benhavn,_Denmark\">København, Denmark</a>"],
	["56", "-6", "<a href=\"https://geohashing.site/geohashing/Tobermory,_United_Kingdom\">Tobermory, United Kingdom</a>"],
	["56", "-5", "<a href=\"https://geohashing.site/geohashing/Oban,_United_Kingdom\">Oban, United Kingdom</a>"],
	["56", "-4", "<a href=\"https://geohashing.site/geohashing/Helensburgh,_United_Kingdom\">Helensburgh, United Kingdom</a>"],
	["56", "-3", "<a href=\"https://geohashing.site/geohashing/Perth,_United_Kingdom\">Perth, United Kingdom</a>"],
	["56", "-2", "<a href=\"https://geohashing.site/geohashing/Dundee,_United_Kingdom\">Dundee, United Kingdom</a>"],
	["56", "-1", "<a href=\"https://geohashing.site/geohashing/North_Sea_56,_-1\">North Sea 56, -1</a>"],
	["56", "-0", "<a href=\"https://geohashing.site/geohashing/North_Sea_56,_-0\">North Sea 56, -0</a>"],
	["56", "0", "<a href=\"https://geohashing.site/geohashing/North_Sea_56,_0\">North Sea 56, 0</a>"],
	["56", "1", "<a href=\"https://geohashing.site/geohashing/North_Sea_56,_1\">North Sea 56, 1</a>"],
	["56", "2", "<a href=\"https://geohashing.site/geohashing/North_Sea_56,_2\">North Sea 56, 2</a>"],
	["56", "3", "<a href=\"https://geohashing.site/geohashing/North_Sea_56,_3\">North Sea 56, 3</a>"],
	["56", "4", "<a href=\"https://geohashing.site/geohashing/North_Sea_56,_4\">North Sea 56, 4</a>"],
	["56", "5", "<a href=\"https://geohashing.site/geohashing/North_Sea_56,_5\">North Sea 56, 5</a>"],
	["56", "6", "<a href=\"https://geohashing.site/geohashing/North_Sea_56,_6\">North Sea 56, 6</a>"],
	["56", "7", "<a href=\"https://geohashing.site/geohashing/North_Sea_56,_7\">North Sea 56, 7</a>"],
	["56", "8", "<a href=\"https://geohashing.site/geohashing/Herning,_Denmark\">Herning, Denmark</a>"],
	["56", "9", "<a href=\"https://geohashing.site/geohashing/Silkeborg,_Denmark\">Silkeborg, Denmark</a>"],
	["56", "10", "<a href=\"https://geohashing.site/geohashing/%C3%85rhus,_Denmark\">Århus, Denmark</a>"],
	["56", "11", "<a href=\"https://geohashing.site/geohashing/Anholt,_Denmark\">Anholt, Denmark</a>"],
	["56", "12", "<a href=\"https://geohashing.site/geohashing/Helsingborg,_Sweden\">Helsingborg, Sweden</a>"],
	["666", "666", ""]
  ];
  /* END generated file from xkcd2js.sh }}} */
