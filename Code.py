
import os
import time
import pandas as pd

from selenium import webdriver
from selenium.webdriver.common.by import By

options = webdriver.ChromeOptions()
options.add_argument('--start-maximized')
options.add_experimental_option('prefs', {
        "download.prompt_for_download": False,
        "download.default_directory" : r"C:\Users\CESAR\Desktop\GitHub",
        "savefile.default_directory": r"C:\Users\CESAR\Desktop\GitHub"})
chromedriver =  r'C:\Program Files\Chromedriver\chromedriver.exe'
os.environ["webdriver.chrome.driver"] = chromedriver

driver = webdriver.Chrome(chromedriver, chrome_options=options)

#Una entrada que tiene esta plataforma es descargar el gasto público que se designa para cada entidad. Existen otras entradas que permiten obtener, 
#por ejemplo, el gasto público que proviene exclusivamente de un impuesto, tributo, entre otros. En este documento se obtiene el gasto público
#que proviene exclusivamente del canon minero. Es posible utilizar el mismo procedimiento para habilitar otras entradas de la misma plataforma.

#Antes de correr, notar que hay dos CANON MINERO y se recomienda correr por separado. 
#Las lineas 42 y 43 se tienen que cambiar por:
        #CANON MINERO "ANTIGUO". Correr desde 2007
        #driver.find_element('xpath',"//*[contains(text(), '2: CANON MINERO')]").click()
#Es posible hacer unos cambios y correr ambos CANON MINERO en un mismo código, pero puede ser más pesado.

for year in range(2012,2022):
        driver.get('https://apps5.mineco.gob.pe/transparencia/Navegador/default.aspx?y=' + str(year) + '&ap=ActProy')
        #Solo hay un frame a diferencia del documento "Web-Scraping-SIAF-1"
        driver.switch_to.frame(0)

        #Rubro
        driver.find_element('xpath','/html/body/form/div[4]/div[3]/div[1]/table/tbody/tr[2]/td[3]/input[2]').click()

        driver.find_element('xpath',"//*[contains(text(), 'CANON Y SOBRECANON')]").click()

        #Tipo de recurso
        driver.find_element('xpath','/html/body/form/div[4]/div[3]/div[1]/table/tbody/tr[2]/td[3]/input[2]').click()

        #CANON MINERO "NUEVO". Correr desde 2008
        driver.find_element('xpath',"//*[contains(text(), 'SUB CUENTA - CANON MINERO')]").click()

        #Nivel de gobierno
        driver.find_element('xpath','/html/body/form/div[4]/div[3]/div[1]/table/tbody/tr[2]/td[1]/input').click()

        driver.find_element('xpath',"//*[contains(text(), 'LOCALES')]").click()

        #Quien gasta. Se divide en dos: 2011 para atras y 2012 para adelante
        if year>=2012:
                #Gob.Loc/Mancon.
                driver.find_element('xpath','/html/body/form/div[4]/div[3]/div[1]/table/tbody/tr[2]/td[1]').click()

                #Departamento
                driver.find_element('xpath','/html/body/form/div[4]/div[3]/div[1]/table/tbody/tr[2]/td[1]/input').click()

        else:
                #Departamento
                driver.find_element('xpath','/html/body/form/div[4]/div[3]/div[1]/table/tbody/tr[2]/td[1]/input[2]').click()

        tabla_dpto = driver.find_element('xpath','/html/body/form/div[4]/div[3]/div[3]/div/table[2]')
        departamentos = tabla_dpto.find_elements(By.TAG_NAME,'tr')
        for dpto in range(len(departamentos)):
                base_dato = []
                driver.find_element('id','tr' + str(dpto)).click()

                #Provincia
                driver.find_element('xpath','/html/body/form/div[4]/div[3]/div[1]/table/tbody/tr[2]/td[1]/input[1]').click()

                tabla_prov = driver.find_element('xpath','/html/body/form/div[4]/div[3]/div[3]/div/table[2]')
                provincias = tabla_prov.find_elements(By.TAG_NAME,'tr')
                for prov in range(len(provincias)):
                        driver.find_element('id','tr' + str(prov)).click()

                        #Distritos
                        driver.find_element('xpath','/html/body/form/div[4]/div[3]/div[1]/table/tbody/tr[2]/td[1]/input').click()

                        tabla_muni = driver.find_element('xpath','/html/body/form/div[4]/div[3]/div[3]/div/table[2]')
                        municipalidades = tabla_muni.find_elements(By.TAG_NAME,'tr')
                        for muni in range(len(municipalidades)):
                                driver.find_element('id','tr' + str(muni)).click()

                                #Especificar generica
                                if year>=2009:
                                        driver.find_element('id','ctl00_CPH1_BtnGenerica').click()
                                else:
                                        driver.find_element('id','ctl00_CPH1_BtnGrupoGasto').click()
                                
                                tabla_generica = driver.find_element('xpath','/html/body/form/div[4]/div[3]/div[3]/div/table[2]')
                                generica = tabla_generica.find_elements(By.TAG_NAME,'tr')
                                for gnrc in range(len(generica)):
                                        driver.find_element('id','tr' + str(gnrc)).click()

                                        if year>=2012:
                                                #Descargar
                                                canon_valor = driver.find_element('xpath','/html/body/form/div[4]/div[3]/div[2]/table/tbody/tr[3]/td[2]').text
                                                dpto_valor = driver.find_element('xpath','/html/body/form/div[4]/div[3]/div[2]/table/tbody/tr[6]/td[2]').text
                                                prov_valor = driver.find_element('xpath','/html/body/form/div[4]/div[3]/div[2]/table/tbody/tr[7]/td[2]').text
                                                dist_valor = driver.find_element('xpath','/html/body/form/div[4]/div[3]/div[2]/table/tbody/tr[8]/td[2]').text

                                                #Seleccionar Funcion
                                                driver.find_element('xpath','/html/body/form/div[4]/div[3]/div[1]/table/tbody/tr[2]/td[2]/input[3]').click()

                                                tabla_funcion = driver.find_element('xpath','/html/body/form/div[4]/div[3]/div[3]/div/table[2]')
                                                funcion = tabla_funcion.find_elements(By.TAG_NAME,'tr')
                                                for fun in range(len(funcion)):
                                                        driver.find_element('id','tr' + str(fun)).click()

                                                        #Seleccionar Division Funcional (este es lo que se conocia como programa en 2011 o antes)
                                                        driver.find_element('xpath','/html/body/form/div[4]/div[3]/div[1]/table/tbody/tr[2]/td[2]/input[3]').click()
                                                        
                                                        tabla_div = driver.find_element('xpath','/html/body/form/div[4]/div[3]/div[3]/div/table[2]')
                                                        division = tabla_div.find_elements(By.TAG_NAME,'tr')
                                                        for div in range(len(division)):
                                                                driver.find_element('id','tr' + str(div)).click()

                                                                #Seleccionar Proyectos
                                                                driver.find_element('xpath','/html/body/form/div[4]/div[3]/div[1]/table/tbody/tr[2]/td[2]/input[2]').click()

                                                                #Descargar
                                                                generica_valor = driver.find_element('xpath','/html/body/form/div[4]/div[3]/div[2]/table/tbody/tr[9]/td[2]').text
                                                                funcion_valor = driver.find_element('xpath','/html/body/form/div[4]/div[3]/div[2]/table/tbody/tr[10]/td[2]').text
                                                                division_valor = driver.find_element('xpath','/html/body/form/div[4]/div[3]/div[2]/table/tbody/tr[11]/td[2]').text

                                                                #Contabilizacion de Proyectos / Actividades
                                                                tabla_proact = driver.find_element('xpath','/html/body/form/div[4]/div[3]/div[3]/div/table[2]')
                                                                proact = tabla_proact.find_elements(By.TAG_NAME,'tr')
                                                                for proyecto in range(1,len(proact),2):
                                                                        proyecto_valor = driver.find_element('xpath','/html/body/form/div[4]/div[3]/div[3]/div/table[2]/tbody/tr[' + str(proyecto) + ']/td[2]').text
                                                                        pia_valor = driver.find_element('xpath','/html/body/form/div[4]/div[3]/div[3]/div/table[2]/tbody/tr[' + str(proyecto) + ']/td[3]').text
                                                                        pim_valor = driver.find_element('xpath','/html/body/form/div[4]/div[3]/div[3]/div/table[2]/tbody/tr[' + str(proyecto) + ']/td[4]').text
                                                                        cer_valor = driver.find_element('xpath','/html/body/form/div[4]/div[3]/div[3]/div/table[2]/tbody/tr[' + str(proyecto) + ']/td[5]').text
                                                                        ca_valor = driver.find_element('xpath','/html/body/form/div[4]/div[3]/div[3]/div/table[2]/tbody/tr[' + str(proyecto) + ']/td[6]').text
                                                                        acm_valor = driver.find_element('xpath','/html/body/form/div[4]/div[3]/div[3]/div/table[2]/tbody/tr[' + str(proyecto) + ']/td[7]').text
                                                                        dev_valor = driver.find_element('xpath','/html/body/form/div[4]/div[3]/div[3]/div/table[2]/tbody/tr[' + str(proyecto) + ']/td[8]').text
                                                                        gir_valor = driver.find_element('xpath','/html/body/form/div[4]/div[3]/div[3]/div/table[2]/tbody/tr[' + str(proyecto) + ']/td[9]').text
                                                                        ava_valor = driver.find_element('xpath','/html/body/form/div[4]/div[3]/div[3]/div/table[2]/tbody/tr[' + str(proyecto) + ']/td[10]').text

                                                                        base_dato.append([year,canon_valor,dpto_valor,prov_valor,dist_valor,generica_valor,funcion_valor,division_valor,
                                                                                proyecto_valor,pia_valor,pim_valor,cer_valor,ca_valor,acm_valor,dev_valor,gir_valor,ava_valor])
                                                                        df = pd.DataFrame(base_dato,columns=['year','canon_valor','dpto_valor','prov_valor','dist_valor','generica_valor','funcion_valor','division_valor',
                                                                                'proyecto_valor','pia_valor','pim_valor','cer_valor','ca_valor','acm_valor','dev_valor','gir_valor','ava_valor'])
                                                                        df.to_csv('A_' + str(year) + '_' + str(dpto) + '.csv',encoding='utf-8-sig',index=False)
                                                                        time.sleep(1)

                                                                #Cambio de division
                                                                driver.find_element('id','ctl00_CPH1_RptHistory_ctl11_TD0').click()

                                                        #Cambio de funcion
                                                        driver.find_element('id','ctl00_CPH1_RptHistory_ctl10_TD0').click()
                                        else:
                                                #Descargar
                                                canon_valor = driver.find_element('xpath','/html/body/form/div[4]/div[3]/div[2]/table/tbody/tr[3]/td[2]').text
                                                dpto_valor = driver.find_element('xpath','/html/body/form/div[4]/div[3]/div[2]/table/tbody/tr[5]/td[2]').text
                                                prov_valor = driver.find_element('xpath','/html/body/form/div[4]/div[3]/div[2]/table/tbody/tr[6]/td[2]').text
                                                dist_valor = driver.find_element('xpath','/html/body/form/div[4]/div[3]/div[2]/table/tbody/tr[7]/td[2]').text

                                                #Seleccionar Programa
                                                driver.find_element('xpath','/html/body/form/div[4]/div[3]/div[1]/table/tbody/tr[2]/td[2]/input[2]').click()

                                                tabla_pro = driver.find_element('xpath','/html/body/form/div[4]/div[3]/div[3]/div/table[2]')
                                                programa = tabla_pro.find_elements(By.TAG_NAME,'tr')
                                                for pro in range(len(programa)):
                                                        driver.find_element('id','tr' + str(pro)).click()

                                                        #Seleccionar Proyectos
                                                        driver.find_element('xpath','/html/body/form/div[4]/div[3]/div[1]/table/tbody/tr[2]/td[2]/input[3]').click()

                                                        #Descargar
                                                        generica_valor = driver.find_element('xpath','/html/body/form/div[4]/div[3]/div[2]/table/tbody/tr[8]/td[2]').text
                                                        funcion_valor = "No hay"
                                                        division_valor = driver.find_element('xpath','/html/body/form/div[4]/div[3]/div[2]/table/tbody/tr[9]/td[2]').text
                                                        #Contabilizacion de Proyectos / Actividades
                                                        tabla_proact = driver.find_element('xpath','/html/body/form/div[4]/div[3]/div[3]/div/table[2]')
                                                        proact = tabla_proact.find_elements(By.TAG_NAME,'tr')
                                                        for proyecto in range(1,len(proact),2):
                                                                proyecto_valor = driver.find_element('xpath','/html/body/form/div[4]/div[3]/div[3]/div/table[2]/tbody/tr[' + str(proyecto) + ']/td[2]').text
                                                                pia_valor = driver.find_element('xpath','/html/body/form/div[4]/div[3]/div[3]/div/table[2]/tbody/tr[' + str(proyecto) + ']/td[3]').text
                                                                pim_valor = driver.find_element('xpath','/html/body/form/div[4]/div[3]/div[3]/div/table[2]/tbody/tr[' + str(proyecto) + ']/td[4]').text
                                                                cer_valor = "No hay"
                                                                ca_valor = "No hay"
                                                                acm_valor = driver.find_element('xpath','/html/body/form/div[4]/div[3]/div[3]/div/table[2]/tbody/tr[' + str(proyecto) + ']/td[5]').text
                                                                dev_valor = driver.find_element('xpath','/html/body/form/div[4]/div[3]/div[3]/div/table[2]/tbody/tr[' + str(proyecto) + ']/td[6]').text
                                                                gir_valor = driver.find_element('xpath','/html/body/form/div[4]/div[3]/div[3]/div/table[2]/tbody/tr[' + str(proyecto) + ']/td[7]').text
                                                                ava_valor = driver.find_element('xpath','/html/body/form/div[4]/div[3]/div[3]/div/table[2]/tbody/tr[' + str(proyecto) + ']/td[8]').text

                                                                base_dato.append([year,canon_valor,dpto_valor,prov_valor,dist_valor,generica_valor,funcion_valor,division_valor,
                                                                        proyecto_valor,pia_valor,pim_valor,cer_valor,ca_valor,acm_valor,dev_valor,gir_valor,ava_valor])
                                                                df = pd.DataFrame(base_dato,columns=['year','canon_valor','dpto_valor','prov_valor','dist_valor','generica_valor','funcion_valor','division_valor',
                                                                        'proyecto_valor','pia_valor','pim_valor','cer_valor','ca_valor','acm_valor','dev_valor','gir_valor','ava_valor'])
                                                                df.to_csv('A_' + str(year) + '_' + str(dpto) + '.csv',encoding='utf-8-sig',index=False)
                                                                time.sleep(1)

                                                        #Cambio de Programa
                                                        driver.find_element('id','ctl00_CPH1_RptHistory_ctl09_TD0').click()

                                        #Cambio de generica
                                        if year>=2012:
                                                driver.find_element('id','ctl00_CPH1_RptHistory_ctl09_TD0').click()
                                        else:
                                                driver.find_element('id','ctl00_CPH1_RptHistory_ctl08_TD0').click()

                                #Cambio de municipalidad
                                if year>=2012:
                                        driver.find_element('id','ctl00_CPH1_RptHistory_ctl08_TD0').click()
                                else:
                                        driver.find_element('id','ctl00_CPH1_RptHistory_ctl07_TD0').click()

                        #Cambio de provincia
                        if year>=2012:
                                driver.find_element('id','ctl00_CPH1_RptHistory_ctl07_TD0').click()
                        else:
                                driver.find_element('id','ctl00_CPH1_RptHistory_ctl06_TD0').click()

                #Cambio de departamento
                if year>=2012:
                        driver.find_element('id','ctl00_CPH1_RptHistory_ctl06_TD0').click()
                else:
                        driver.find_element('id','ctl00_CPH1_RptHistory_ctl05_TD0').click()

driver.close()