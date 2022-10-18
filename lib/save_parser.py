from lib.bouncy_boi import *
from lxml import etree as ET
import os
import shutil

class SaveParser():
    def __init__(self, dir: str) -> None:
        self.file_str = dir
        self.file_str = os.path.join("saves", self.file_str)
        self.file = None
        self.output = None
        self.root = None

    def makDir(self):
        if os.path.exists(self.file_str):
            shutil.rmtree(self.file_str)
        os.makedirs(self.file_str)

    def open(self):
        self.file = open(self.file_str+"\\save.xml", "w")
    def close(self):
        self.file.close()

    def load(self):
        dvds = []
        xml = self.loadXML()
        if xml is None: return
        bins = self.loadBin()
        for i in range(len(xml)):
            dvds.append(
                {"bin": bins[i], "x": xml[i].get("x"), "y": xml[i].get("y"), "vx": xml[i].get("vx"), "vy": xml[i].get("vy")}
            )
        return dvds

    def loadXML(self):
        try:
            self.root = ET.parse(self.file_str+"\\save.xml")
        except:
            pass
        if self.root is None:
            return
        dvds = []
        for dvd in self.root.findall("dvd"):
            dvds.append(dvd)
        return dvds

    def loadBin(self):
        files = os.listdir(self.file_str)
        bins = []
        for file in files:
            ext = file.split(".")[1]
            if ext == "ass":
                bin_path = os.path.join(self.file_str, file)
                f = open(bin_path, "rb")
                bins.append(f.read())
        return bins

    def write(self):
        self.file.write(self.output)

    def toStr(self):
        self.output = ET.tostring(self.root, encoding="unicode")

    def save(self, dvds):
        self.makDir()

        self.root = ET.Element("dvds")
        dvd_bytes = ""
        i=0
        for dvd in dvds:
            element = ET.SubElement(self.root, "dvd", attrib={"x": str(dvd.x), "y": str(dvd.y), "vx": str(dvd.vx), "vy": str(dvd.vy)})
            self.saveBin(dvd.bytes, i)
            i += 1
        
        self.open()
        self.toStr()
        self.write()
        self.close()

    def saveBin(self, dvd_bytes, i):
        bin_path = os.path.join(self.file_str, f"{i}.ass")
        f = open(bin_path, "wb")
        f.write(dvd_bytes)
        f.close()