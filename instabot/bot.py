from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import random
import sys


class InstagramBot:
    seguidores_perfil = []
    pic_hrefs = []
    numero_perfis_atual = 0
    numero_fotos = 0
    contador_para_comentar = 1

    def __init__(self, username, password, stdout, linguagem, navegador):
        self.username = username
        self.password = password
        self.stdout = stdout
        self.driver = eval(navegador)
        self.linguagem = linguagem
        if linguagem == '1':
            self.like = 'Like'
            self.post = 'Post'
            self.unlike = 'Unlike'
        else:
            self.like = 'Curtir'
            self.post = 'Publicar'
            self.unlike = 'Descurtir'

    @staticmethod
    def digite_como_pessoa(frase, onde_digitar):
        for letra in frase:
            onde_digitar.send_keys(letra)
            time.sleep(random.randint(1, 8) / 30)

    @staticmethod
    def comentario_aleatorio(x, y, z):
        """
        :param x: grupo de palavra inicial
        :param y: grupo de palavra secundaria
        :param z: emoji
        :return: uma frase sendo: (x + y) ou (x + z) ou (y + z)
        """
        option = random.randrange(3)
        if option == 0:
            return random.choice(x) + random.choice(y)
        elif option == 1:
            return random.choice(y) + random.choice(z)
        else:
            return random.choice(x) + random.choice(z)

    def login(self):
        driver = self.driver
        driver.get("https://www.instagram.com/")
        time.sleep(5)
        user_name_elem = driver.find_element_by_xpath("//input[@name='username']")
        user_name_elem.clear()
        user_name_elem.send_keys(self.username)
        passworword_elem = driver.find_element_by_xpath("//input[@name='password']")
        passworword_elem.clear()
        passworword_elem.send_keys(self.password)
        passworword_elem.send_keys(Keys.RETURN)
        time.sleep(6)

    def selecionar_fotos_hashtags(self, hashtag):
        driver = self.driver
        driver.get("https://www.instagram.com/explore/tags/" + hashtag + "/")
        time.sleep(2)

        for _ in range(1, 7):
            try:
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(2)
                hrefs_na_tela = driver.find_elements_by_tag_name('a')
                hrefs_na_tela = [elem.get_attribute('href') for elem in hrefs_na_tela
                                 if '.com/p/' in elem.get_attribute('href')]
                [self.pic_hrefs.append(href) for href in hrefs_na_tela if href not in self.pic_hrefs]
            except Exception:
                continue

    def listar_perfis_do_perfil(self, perfilrandom):
        driver = self.driver
        driver.get("https://www.instagram.com/" + perfilrandom + "/")
        time.sleep(2)
        self.driver.find_element_by_xpath("//a[@href= \"/" + perfilrandom + "/followers/\"" + "]").click()
        time.sleep(1)
        driver.find_element_by_class_name('PZuss').click()
        for _ in range(1, 10):
            try:
                driver.execute_script('''
                    var fDialog = document.querySelector('div[role="dialog"] .isgrP');
                    fDialog.scrollTop = fDialog.scrollHeight
                ''')
                time.sleep(4)
                hrefs_na_tela = driver.find_elements_by_tag_name('a')
                hrefs_na_tela = [elem.get_attribute('href') for elem in hrefs_na_tela
                                 if 'FPmhX notranslate  _0imsa ' in elem.get_attribute('class')]
                [self.seguidores_perfil.append(href) for href in hrefs_na_tela if href not in self.seguidores_perfil]
            except Exception:
                continue

    def selecionar_fotos_perfil(self):
        driver = self.driver
        perfil_do_perfil = random.choice(self.seguidores_perfil)
        driver.get(perfil_do_perfil)
        time.sleep(2)
        limite_fotos = 0
        max_fotos = random.randrange(3, 7)

        for _ in range(1, 2):  # Esse 'for' existe para facilitar novas funcionalidades
            try:
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(2)
                hrefs_na_tela = driver.find_elements_by_tag_name('a')
                hrefs_na_tela = [elem.get_attribute('href') for elem in hrefs_na_tela
                                 if '.com/p/' in elem.get_attribute('href')]
                self.numero_perfis_atual += 1
                for href in hrefs_na_tela:
                    if href not in self.pic_hrefs and limite_fotos < max_fotos:
                        self.pic_hrefs.append(href)
                        limite_fotos += 1
            except Exception:
                continue
        self.seguidores_perfil.remove(perfil_do_perfil)

    def comentar_fotos(self, x, y, z, comentario=None):
        driver = self.driver
        for foto_atual in self.pic_hrefs:
            driver.get(foto_atual)
            time.sleep(5)
            try:
                comentario = driver.find_element_by_xpath(f"//a[contains(text(),'{self.username}')]")
            except:
                pass
            if comentario is None:
                try:
                    time.sleep(random.randint(2, 4))
                    driver.find_element_by_class_name('Ypffh').click()
                    campo_comentario = driver.find_element_by_class_name('Ypffh')
                    time.sleep(random.randint(2, 4))
                    try:
                        self.digite_como_pessoa(self.comentario_aleatorio(x, y, z), campo_comentario)
                    except:
                        pass
                    time.sleep(random.randint(10, 20))
                    driver.find_element_by_xpath(f"//button[contains(text(),'{self.post}')]").click()
                    self.numero_fotos += 1
                    self.contador_stdout()
                    time.sleep(random.randint(367, 603))
                except Exception:
                    time.sleep(5)
            time.sleep(5)
            comentario = None

    def like_foto(self, unlike=None):
        driver = self.driver
        for foto_atual in self.pic_hrefs:
            driver.get(foto_atual)
            try:
                time.sleep(4)
                unlike = self.driver.find_element_by_xpath("//*[@aria-label='{}']".format(self.unlike))
            except Exception:
                pass
            if unlike is None:
                try:
                    time.sleep(random.randint(6, 12))
                    self.driver.find_element_by_xpath("//*[@aria-label='{}']".format(self.like)).click()
                    self.numero_fotos += 1
                    self.contador_stdout()
                    time.sleep(random.randint(45, 59))
                except Exception:
                    time.sleep(5)
            time.sleep(3)
            unlike = None

    def like_comentar(self, x, y, z, unlike=None):
        driver = self.driver

        for foto_atual in self.pic_hrefs:
            driver.get(foto_atual)
            try:
                time.sleep(4)
                unlike = self.driver.find_element_by_xpath("//*[@aria-label='{}']".format(self.unlike))
            except Exception:
                pass
            if unlike is None:
                if self.contador_para_comentar % 10 == 0:
                    try:
                        time.sleep(random.randint(2, 10))
                        driver.find_element_by_class_name('Ypffh').click()
                        campo_comentario = driver.find_element_by_class_name('Ypffh')
                        time.sleep(random.randint(2, 4))
                        try:
                            self.digite_como_pessoa(self.comentario_aleatorio(x, y, z), campo_comentario)
                        except Exception:
                            pass
                        try:
                            time.sleep(2)
                            driver.find_element_by_xpath(f"//button[contains(text(),'{self.post}')]").click()
                            time.sleep(random.randint(10, 20))
                        except:
                            self.contador_para_comentar -= 1
                            pass
                    except Exception:
                        time.sleep(2)
                try:
                    time.sleep(random.randint(6, 12))
                    self.driver.find_element_by_xpath("//*[@aria-label='{}']".format(self.like)).click()
                    self.numero_fotos += 1
                    self.contador_stdout()
                    time.sleep(random.randint(45, 59))
                    self.contador_para_comentar += 1
                except Exception:
                    time.sleep(5)
            time.sleep(3)
            unlike = None

    def tabela_stdout(self):
        if self.stdout == 'com_hashtags(hashtags, tipo_busca, primeira_palavra, complemento, ' \
                          'emoji, username, password, modo_bot, linguagem, navegador)':
            print('----------------------------------------')
            print('|Nº - Fotos Faltando |Nº - Fotos Atual | ')
        elif self.stdout == 'com_perfil(perfis, tipo_busca, primeira_palavra, complemento, ' \
                            'emoji, username, password, modo_bot, linguagem, navegador)':
            print('-------------------------------------------------------------------')
            print('|Nº - Perfis Faltando | Nº - Perfis Visitados | Nº - Fotos Atual  |')

    def contador_stdout(self):
        for _ in range(150):
            if self.stdout == 'com_hashtags(hashtags, tipo_busca, primeira_palavra, complemento, ' \
                              'emoji, username, password, modo_bot, linguagem, navegador)':
                sys.stdout.write(f"\r         {len(self.pic_hrefs) - self.numero_fotos}          |"
                                 f"        {self.numero_fotos}      |")
                sys.stdout.flush()
                time.sleep(0.5)
            elif self.stdout == 'com_perfil(perfis, tipo_busca, primeira_palavra, complemento, ' \
                                'emoji, username, password, modo_bot, linguagem, navegador)':
                sys.stdout.write(
                    f"\r           {len(self.seguidores_perfil)}         |"
                    f"          {self.numero_perfis_atual}          |"
                    f"        {self.numero_fotos}        | ")
                sys.stdout.flush()
                time.sleep(0.5)

    def limpar_urefs(self):
        self.pic_hrefs.clear()

    def deu_ruim(self):
        self.driver.close()
        print('\nAlgo está errado! Por segurança, o programa foi finalizado.\n')
        sys.exit()

    def close_browser(self):
        self.driver.close()
