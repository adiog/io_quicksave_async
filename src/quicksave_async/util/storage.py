# This file is a part of quicksave project.
# Copyright (c) 2017 Aleksander Gajewski <adiog@quicksave.io>.

import os

import sys
import subprocess
import getpass
import shutil


class StorageFactory(object):
    @classmethod
    def create(cls, connection_string, user_hash, keys):
        if 'sshfs://' in connection_string:
            return Sshfs(connection_string, user_hash, keys)
        elif 'file://' in connection_string:
            print(connection_string[7:])
            return LocalStorage(connection_string[7:])
        else:
            raise RuntimeError()


class LocalStorage(object):
    def __init__(self, path):
        self.path = path

    def getMetaPath(self, metaHash):
        return self.path + "/" + metaHash[0:2] + "/" + metaHash[2:4] + "/" + metaHash[4:]

    def getFilePath(self, metaHash, filename):
        return self.getMetaPath(metaHash) + filename

    def init(self, metaHash):
        metaPath = self.getMetaPath(metaHash)
        os.makedirs(metaPath, exist_ok=True)
        try:
            subprocess.check_output(['mkdir', '-p', metaPath])
        except:
            pass

    def store(self, meta, filepath, filename):
        item_dir = self.getMetaPath(meta.meta_hash)
        output_file = item_dir + '/' + filename
        self.move(filepath, output_file)

    def save(self, metaHash, filename, filebody):
        filePath = self.getFilePath(metaHash, filename)
        with open(filePath, 'w') as f:
            f.write(filebody)

    def read(self, fileBean):
        filePath = self.getFilePath(fileBean.meta_hash, fileBean.filename)
        with open(filePath, 'r') as f:
            return f.read()

    def remove(self, metaHash, fileName=None):
        if fileName is not None:
            shutil.rmtree(self.getMetaPath(metaHash))
        else:
            shutil.rmtree(self.getFilePath(metaHash, fileName))

    def move(self, source, target):
        shutil.move(source, target)


class Sshfs(LocalStorage):
    def __init__(self, connectionString, user_hash, keys):
        if 'sshfs://' not in connectionString:
            raise RuntimeError()
        else:
            connectionString = connectionString[8:]

        splitConnectionString = connectionString.split(' ')

        params = {}
        for param in splitConnectionString:
            splitParam = param.split('=')
            params[splitParam[0]] = splitParam[1]

        keyPath = "/keys/%s_id_rsa" % user_hash
        sshPath = "/sshfs/%s" % user_hash

        for key in keys:
            if params['key'] == key.name:
                if not os.path.exists(keyPath):
                    with open(keyPath, 'w') as keyFile:
                        keyFile.write(key.value)
                        keyFile.write('\n')
                    os.chmod(keyPath, 600)
                    subprocess.check_output(['chmod', '600', keyPath])

        os.makedirs(sshPath, exist_ok=True)

        check_mount = 'mountpoint -q %s' % sshPath
        try:
            check = subprocess.check_call(check_mount.split(' '))
        except subprocess.CalledProcessError:
            check = 1
        if (check != 0):
            command = "sshfs -o IdentityFile=%s -o idmap=user -p %s %s@%s:%s %s" % (keyPath, params['port'], params['user'], params['host'], params['path'], sshPath)
            subprocess.check_output(command.split(' '))

        super().__init__(sshPath)
        self.owner = params['user']

    def move(self, src, tgt):
        command = 'rsync --remove-source-files --usermap=%s:%s %s %s' % (self.owner, getpass.getuser(), src, tgt)
        subprocess.check_output(command.split(' '))

