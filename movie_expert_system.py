import pandas as pd
import numpy as np

import matplotlib.pyplot as plt
import numpy as np

from fuzzy_expert.variable import FuzzyVariable
from fuzzy_expert.rule import FuzzyRule
from fuzzy_expert.inference import DecompositionalInference

from tkinter import ttk
from tkinter import *

class Aplicacion:
    #Constructor
    def __init__(self, window):
        #Variables maquina de inferencia
        self.respuesta = ""
        self.state = 0
        self.preguntas = [
            "Quieres ver pelicula/serie de accion?",
            "Quieres ver pelicula/serie de aventura?",
            "Quieres ver pelicula/serie de comedia?",
            "Quieres ver un short?",
            "Quieres ver pelicula/serie de familiar?",
            "Quieres ver pelicula/serie de romance?",
            "Quieres ver pelicula/serie de drama?",
            "Quieres ver pelicula de fantasia",
            "Quieres ver una pelicula/serie excelente?",
            "Quieres ver una pelicula/serie buena?",
            "Quieres ver una pelicula/serie dominguera?",

        ]
        self.vars_respuesta = []
        self.df = pd.read_csv(r"data\Top 50 Animation Movies and TV Shows.csv")

        # Initializations 
        self.wind = window
        self.wind.title('Expert Engine')
        self.wind.columnconfigure(0, weight=1)
        self.wind.rowconfigure(0, weight=1)


        # Creating a Frame Container 
        frame = LabelFrame(self.wind, text = 'Clasificador Series/Peliculas de animacion por categoria/rating')
        frame.grid(row = 0, column = 0, pady = 20,padx=20)


      
        self.pregunta = Label(frame, text = '')
        self.pregunta.grid(row = 1, column = 0,columnspan=5)
        self.pregunta.grid_remove()


        ttk.Button(frame, text = 'Si', command = self.selec_si).grid(row=2,column=0,pady=25)
        ttk.Button(frame, text = 'Talvez si', command = self.selec_talvez_si).grid(row=2, column=1,pady=25)
        ttk.Button(frame, text = 'No se', command = self.selec_no_se).grid(row=2, column=2,pady=25)
        ttk.Button(frame, text = 'Casi no', command = self.selec_casi_no).grid(row=2, column=3,pady=25)
        ttk.Button(frame, text = 'No', command = self.selec_no).grid(row=2, column=4,pady=25)

        self.nextboton = ttk.Button(frame, text = 'Empezar Preguntas', command = self.nextbutton)
        self.nextboton.grid(row = 7, columnspan = 5,pady = 15)

        self.content = Label(frame, text = '')
        self.content.grid(row = 8, column = 0, pady = 10,columnspan=5)
        self.content.grid_remove()

        #Varaibles de logica difusa
        self.variables_categoria = {
            "Action": FuzzyVariable(
                universe_range=(0,100),
                terms={
                    "si_Action": ('trapmf', 9,10,19,20),
                    "no_Action":('trapmf', 19,20,89,90),
                    #"dolmildiez": ('trapmf', 2010,2011, 2022, 2023),
                },
            ),
            "Adventure": FuzzyVariable(
                universe_range=(0,100),
                terms={
                    "si_Adventure":('trapmf', 19,20, 29, 30),
                    "no_Adventure":[(9,0.0),(10,1.0),(19,1.0),(20,0.0),(29,0.0),(30,1.0),(89,1.0),(90,0.0)],
                },
            ),
            "Comedy": FuzzyVariable(
                universe_range=(0,100),
                terms={
                    "si_Comedy": ('trapmf', 29,30, 39,40 ),
                    "no_Comedy": [(9,0.0),(10,1.0),(29,1.0),(30,0.0),(39,0.0),(40,1.0),(89,1.0),(90,0.0)],
                },
            ),
            "Short": FuzzyVariable(
                universe_range=(0,100),
                terms={
                    "si_Short": ('trapmf', 39,40, 49,50 ),
                    "no_Short": [(9,0.0),(10,1.0),(39,1.0),(40,0.0),(49,0.0),(50,1.0),(89,1.0),(90,0.0)],
                },
            ),
            "Family": FuzzyVariable(
                universe_range=(0,100),
                terms={
                    "si_Family": ('trapmf', 49,50, 59,60 ),
                    "no_Family": [(9,0.0),(10,1.0),(49,1.0),(50,0.0),(59,0.0),(60,1.0),(89,1.0),(90,0.0)],
                },
            ),
            "Romance": FuzzyVariable(
                universe_range=(0,100),
                terms={
                    "si_Romance": ('trapmf', 59,60, 69,70 ),
                    "no_Romance": [(9,0.0),(10,1.0),(59,1.0),(60,0.0),(69,0.0),(70,1.0),(89,1.0),(90,0.0)],
                },
            ),
            "Drama": FuzzyVariable(
                universe_range=(0,100),
                terms={
                    "si_Drama": ('trapmf', 69,70, 79,80 ),
                    "no_Drama": [(9,0.0),(10,1.0),(69,1.0),(70,0.0),(79,0.0),(80,1.0),(89,1.0),(90,0.0)],
                },
            ),
            "Fantasy": FuzzyVariable(
                universe_range=(0,100),
                terms={
                    "si_Fantasy": ('trapmf', 79,80, 89,90 ),
                    "no_Fantasy": ('trapmf', 9,10,79,80),
                },
            ),
            
        }

        self.variables_rating = {
            "Excelente": FuzzyVariable(
                universe_range=(0,10),
                terms={
                    "si_Excelente": ('trapmf', 8.9,9,9.7,9.8),
                    "no_Excelente":('trapmf', 0,0.1,8.9,9),
                },
            ),
            "Buena": FuzzyVariable(
                universe_range=(0,10),
                terms={
                    "si_Buena":('trapmf', 8.3,8.4,8.9,9),
                    "no_Buena":[(0,0.0),(0.1,1.0),(8.3,1.0),(8.4,0.0),(8.9,0.0),(9,1.0),(9.7,1.0),(9.8,0.0)],
                },
            ),
            "dominguera": FuzzyVariable(
                universe_range=(0,10),
                terms={
                    "si_dominguera": ('trapmf', 6.35,6.45,8.3,8.4),
                    "no_dominguera": [(0, 0.0),(0.1,1.0),(6.35,1.0),(6.45,0.0),(8.3,0.0),(8.4,1.0),(9.7,1.0),(9.8,0.0)],
                },
            ),
            "mala": FuzzyVariable(
                universe_range=(0,10),
                terms={
                    "si_mala": ('trapmf',0,0.1,6.35,6.45),
                    "no_mala": ('trapmf', 6.35,6.45,9.7,9.8),
                },
            ),
            
        }

        self.variables_intermedias = {
            "decision_categoria": FuzzyVariable(
                universe_range=(0, 10),
                terms={
                    "no": ('trapmf', 0,0.2,1.8, 2),
                    "casino":('trapmf', 2,2.2, 3.8, 4.0),
                    "nose": ('trapmf', 4.0,4.2, 5.8, 6.0),
                    "talvezsi": ('trapmf', 6.0,6.2, 7.8, 8.0),
                    "si": ('trapmf', 8.0,8.2, 9.8, 10.0),
                },
            ),
            
            "decision_rating": FuzzyVariable(
                universe_range=(0, 10),
                terms={
                    "no": ('trapmf', 0,0.2,1.8, 2),
                    "casino":('trapmf', 2,2.2, 3.8, 4.0),
                    "nose": ('trapmf', 4.0,4.2, 5.8, 6.0),
                    "talvezsi": ('trapmf', 6.0,6.2, 7.8, 8.0),
                    "si": ('trapmf', 8.0,8.2, 9.8, 10.0),
                },
            ),
        }
        self.variable_global = {
            "decision": FuzzyVariable(
                universe_range=(0, 9),
                terms={
                    "no": ('trapmf', 0,0.2,0.8, 1),
                    "no_casino": ('trapmf', 1,1.2,1.8, 2),
                    "casino":('trapmf', 2,2.2, 2.8, 3.0),
                    "nose_casino":('trapmf', 3,3.2, 3.8, 4.0),
                    "nose": ('trapmf', 4.0,4.2, 4.8, 5.0),
                    "talvezsi_nose": ('trapmf', 5.0,5.2, 5.8, 6.0),
                    "talvezsi": ('trapmf', 6.0,6.2, 6.8, 7.0),
                    "talvezsi_si": ('trapmf', 7.0,7.2, 7.8, 8.0),
                    "si": ('trapmf', 8.0,8.2, 8.8, 9.0),

                        
                },
            ),
        }
        self.variables = self.variables_categoria | self.variables_rating| self.variables_intermedias
        self.macro_variables = self.variables_intermedias | self.variable_global 

        self.macro_rules = [
            FuzzyRule(
                premise=[
                    ("decision_rating", "si"),
                    ("AND", "decision_categoria", "si"),
                ],
                consequence=[("decision", "si")],
            ),
            FuzzyRule(
                premise=[
                    ("decision_rating", "talvezsi"),#
                    ("AND", "decision_categoria", "si"),
                ],
                consequence=[("decision", "talvezsi_si")],
            ),
            FuzzyRule(
                premise=[
                    ("decision_rating", "talvezsi"),
                    ("AND", "decision_categoria", "talvezsi"),
                ],
                consequence=[("decision", "talvezsi")],
            ),
            FuzzyRule(
                premise=[
                    ("decision_rating", "nose"),
                    ("AND", "decision_categoria", "si"),
                ],
                consequence=[("decision", "talvezsi")],
            ),
            FuzzyRule(
                premise=[
                    ("decision_rating", "nose"),#
                    ("AND", "decision_categoria", "talvezsi"),
                ],
                consequence=[("decision", "talvezsi_nose")],
            ),
            FuzzyRule(
                premise=[
                    ("decision_rating", "nose"),
                    ("AND", "decision_categoria", "nose"),
                ],
                consequence=[("decision", "nose")],
            ),
            FuzzyRule(
                premise=[
                    ("decision_rating", "casino"), #
                    ("AND", "decision_categoria", "nose"),
                ],
                consequence=[("decision", "nose_casino")],
            ),
            FuzzyRule(
                premise=[
                    ("decision_rating", "casino"),
                    ("AND", "decision_categoria", "casino"),
                ],
                consequence=[("decision", "casino")],
            ),
            FuzzyRule(
                premise=[
                    ("decision_rating", "no"),
                    ("AND", "decision_categoria", "nose"),
                ],
                consequence=[("decision", "casino")],
            ),
            FuzzyRule(
                premise=[
                    ("decision_rating", "no"),#
                    ("AND", "decision_categoria", "casino"),
                ],
                consequence=[("decision", "no_casino")],
            ),
            FuzzyRule(
                premise=[
                    ("decision_rating", "no"),
                    ("AND", "decision_categoria", "no"),
                ],
                consequence=[("decision", "no")],
            ),
        ]
        
    def selec_si(self):
        self.respuesta = "si"
    def selec_talvez_si(self):
        self.respuesta = "talvezsi"
    def selec_no_se(self):
        self.respuesta = "nose"
    def selec_casi_no(self):
        self.respuesta = "casino"
    def selec_no(self):
        self.respuesta = "no"
    
     
    def nextbutton(self):
        if self.state == 0:
            self.content.grid_remove()
            self.nextboton["text"]="Siguiente Pregunta"
            self.pregunta["text"]=self.preguntas[0]
            self.pregunta.grid()
        elif self.state < len(self.preguntas):
            self.pregunta["text"]=self.preguntas[self.state]
            self.vars_respuesta.append(self.respuesta)
            print("Entro a preguntas")
        elif self.state == len(self.preguntas):
            self.vars_respuesta.append(self.respuesta)
            self.pregunta["text"]="Las preguntas se acabaron"
            self.nextboton["text"]="Generar Recomendaciones"
            print("Entro a generar recomendaciones")
            print(self.vars_respuesta)
            
        
        if self.state > len(self.preguntas):
            resultado = self.motordeInferencias()
            publish = []
            probabilidad = 0.0
            if len(resultado["100"]) != 0:
                publish = resultado["100"]
                probabilidad = 95.0
            elif len(resultado["90"]) != 0:
                publish = resultado["90"]
                probabilidad = 90.0
            elif len(resultado["80"]) != 0:
                publish = resultado["80"]
                probabilidad = 80.0
            elif len(resultado["65"]) != 0:
                publish = resultado["65"]
                probabilidad = 65.0
         
            testo_resultado = f"Estas son las recomendaciones de acuerdo a sus preferencias\ncon un factor de certeza del {probabilidad} porciento:\n\n"
            for element in publish:
                testo_resultado = testo_resultado + element + "\n"
            self.content["text"] = testo_resultado
            self.content.grid()
            self.pregunta.grid_remove()
            self.nextboton["text"]="Iniciar de nuevo"
            self.vars_respuesta = []
            self.state = 0
        else:
            self.state +=1

    def motordeInferencias(self):
        inputs_categoria = [
            ('Action',self.vars_respuesta[0]),
            ('Adventure',self.vars_respuesta[1]),
            ('Comedy',self.vars_respuesta[2]),
            ('Short',self.vars_respuesta[3]),
            ('Family',self.vars_respuesta[4]),
            ('Romance',self.vars_respuesta[5]),
            ('Drama',self.vars_respuesta[6]),
            ('Fantasy',self.vars_respuesta[7]),
            ]
        premisas_categoria = self.createRules(inputs_categoria,prefix="OR")
        inputs_rating = [
            ('Excelente',self.vars_respuesta[8]),
            ('Buena',self.vars_respuesta[9]),
            ('dominguera',self.vars_respuesta[10]),
            ('mala',"no"),
        ]
        
        premisas_rating = self.createRules(inputs_rating,prefix="OR")
        #Creacion de reglas
        rules_categoria = self.reglas(premisas_categoria,"decision_categoria")
        rules_rating = self.reglas(premisas_rating,"decision_rating")
        self.rules = rules_categoria+ rules_rating

        self.model = DecompositionalInference(
            and_operator="min",
            or_operator="max",
            implication_operator="Rc",
            composition_operator="max-min",
            production_link="max",
            defuzzification_operator="cog",
        )

        #Tratamiento de la data

        cleanData = {
            'Rating':self.df.loc[:,'Rating'],
            'genre':self.df.loc[:,'genre'],
        }
        nameFrame = iter(self.df.loc[:,"Name"])
        res = self.segmentarPeliculas(cleanData,nameFrame)
        return res

    def segmentarPeliculas(self,data,Nameframe):
        segmentacion = {"100": [], "90": [],"80": [],"65":[],"50": [],"35":[],"25": [],"10":[],"0": [],}
        nombre = Nameframe #iter(dataframe.loc[:,"Name"])
        
        rating_iter = data['Rating']
        genre_iter = data['genre']

        for element in range(0,46): #tamaño fijo del dataset
            #Descomposion de la data
            
            rating = rating_iter[element]
            genre = genre_iter[element]
        
            #Parametros del modelo
            
            parametros_categoria = {
            'Action':0.0,
            'Adventure':0.0,
            'Comedy':0.0,
            'Short':0.0,
            'Family':0.0,
            'Romance':0.0,
            'Drama':0.0,
            'Fantasy':0.0,
            }
            values = {
                'Action':15.0,
                'Adventure':25.0,
                'Comedy':35.0,
                'Short':45.0,
                'Family':55.0,
                'Romance':65.0,
                'Drama':75.0,
                'Fantasy':85.0,
            }
             #Descomposion de la data
            for cadena in genre.split(", "):
                parametros_categoria[cadena]=values[cadena]

            parametros_rating = {
                'Excelente':rating,
                'Buena':rating,
                'dominguera':rating,
                'mala':rating,
            }

            #Calculo del modelo
            sub_result = self.model(
                variables=self.variables,
                rules=self.rules,
                **parametros_categoria,
                **parametros_rating,
                )
            result = self.model(
                variables=self.macro_variables,
                rules=self.macro_rules,
                **sub_result[0]
            )
            
            result = result[0]['decision']
            if result > 8.0:
                segmentacion["100"].append(next(nombre))#,result))#,sub_result))
            elif 7.0 < result < 8.0:
                segmentacion["90"].append(next(nombre))#,result))#,sub_result))
            elif 6.0 < result < 7.0:
                segmentacion["80"].append(next(nombre))#,result))#,sub_result))
            elif 5.0 < result < 6.0:
                segmentacion["65"].append(next(nombre))#result))#,sub_result))
            elif 4.0 < result < 5.0:
                segmentacion["50"].append(next(nombre))#result))#,sub_result))
            elif 3.0 < result < 4.0:
                segmentacion["35"].append(next(nombre))#result))#,sub_result))
            elif 2.0 < result < 3.0:
                segmentacion["25"].append(next(nombre))#result))#,sub_result))
            elif 1.0 < result < 2.0:
                segmentacion["10"].append(next(nombre))#result))#,sub_result))
            elif 0.0 < result < 1.0:
                segmentacion["0"].append(next(nombre))#result))#,sub_result))
        return segmentacion
    

    def createRules(self,dataUsuario,prefix="OR"):
        usedValues = []
        premises = {}

        
        
        for etiqueta, categoria in dataUsuario:
            if categoria not in usedValues:
                usedValues.append(categoria)
                premises[categoria] = [(etiqueta,f"si_{etiqueta}")] 

            else:
                if isinstance(prefix,dict):
                    premises[categoria].append((prefix[categoria],etiqueta,f"si_{etiqueta}"))
                elif isinstance(prefix,str):
                    premises[categoria].append((prefix,etiqueta,f"si_{etiqueta}"))
                else:
                    raise ValueError("prefix only accept str and list type")
        return premises
    
    def reglas(self,premisas,consecuencia):
        reglas = []
        for keys,value in premisas.items():
            reglas.append(
                FuzzyRule(
                premise=value,
                consequence=[(consecuencia, keys)],
            )
            )
        return reglas

        
if __name__ == '__main__':
    window = Tk()
    application = Aplicacion(window)
    window.mainloop()
