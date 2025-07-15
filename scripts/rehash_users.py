#!/usr/bin/env python3
"""
One-off script to rehash all existing User.password fields to MD5.
"""
import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))) 
from models import storage
from models.user import User

def rehash_all_users():
    all_users = storage.all(User).values()
    for user in all_users:
        raw = user.password       # this is currently clear-text
        user.password = raw       # setter will MD5 it
    storage.save()
    print(f"Rehashed {len(all_users)} users.")

if __name__ == '__main__':
    rehash_all_users()
    storage.close()

