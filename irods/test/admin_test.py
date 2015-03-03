#! /usr/bin/env python
import unittest
import os
import sys

from irods.models import User
from irods.session import iRODSSession
from irods.exception import UserDoesNotExist
import config




class TestAdmin(unittest.TestCase):
    '''Suite of tests on admin operations
    '''
    
    # test data
    new_user_name = 'bobby'
    new_user_type = 'rodsuser'
    new_user_zone = config.IRODS_SERVER_ZONE    # use remote zone when creation is supported
    
    

    def setUp(self):
        self.sess = iRODSSession(host=config.IRODS_SERVER_HOST,
                                 port=config.IRODS_SERVER_PORT,
                                 user=config.IRODS_USER_USERNAME,
                                 password=config.IRODS_USER_PASSWORD,
                                 zone=config.IRODS_SERVER_ZONE)
        

        
    def tearDown(self):
        '''Close connections
        '''
        self.sess.cleanup()


    def test_create_and_delete_local_user(self):
        """
        """
        # user should not be already present
        self.assertRaises(UserDoesNotExist, lambda: self.sess.users.get(self.new_user_name))
        
        # create user
        self.sess.users.create(self.new_user_name, self.new_user_type)
        
        # retrieve user
        user = self.sess.users.get(self.new_user_name)
        repr(user)  # for coverage
        
        # assertions
        self.assertEqual(user.name, self.new_user_name)
        self.assertEqual(user.zone, config.IRODS_SERVER_ZONE)
        
        # delete user
        self.sess.users.remove(self.new_user_name)

        # user should be gone
        self.assertRaises(UserDoesNotExist, lambda: self.sess.users.get(self.new_user_name))


    def test_create_and_delete_user_with_zone(self):
        """
        """
        # user should not be already present
        self.assertRaises(UserDoesNotExist, lambda: self.sess.users.get(self.new_user_name, self.new_user_zone))
        
        # create user
        self.sess.users.create(self.new_user_name, self.new_user_type, self.new_user_zone)
        
        # retrieve user
        user = self.sess.users.get(self.new_user_name, self.new_user_zone)
        
        # assertions
        self.assertEqual(user.name, self.new_user_name)
        self.assertEqual(user.zone, self.new_user_zone)
        
        # delete user
        self.sess.users.remove(self.new_user_name, self.new_user_zone)

        # user should be gone
        self.assertRaises(UserDoesNotExist, lambda: self.sess.users.get(self.new_user_name, self.new_user_zone))
    
    
    def test_modify_user_type(self):
        # make new regular user
        self.sess.users.create(self.new_user_name, self.new_user_type)
        
        # check type
        row = self.sess.query(User.type).filter(User.name == self.new_user_name).one()
        self.assertEqual(row[User.type], self.new_user_type)
        
        # change type to rodsadmin
        self.sess.users.modify(self.new_user_name, 'type', 'rodsadmin')
        
        # check type again
        row = self.sess.query(User.type).filter(User.name == self.new_user_name).one()
        self.assertEqual(row[User.type], 'rodsadmin')

        # delete user
        self.sess.users.remove(self.new_user_name)

        # user should be gone
        self.assertRaises(UserDoesNotExist, lambda: self.sess.users.get(self.new_user_name))

    
    @unittest.skip('needs additional massaging in manager')
    def test_set_user_password(self):
        # make new regular user
        self.sess.users.create(self.new_user_name, self.new_user_type)
        
        # set password
        #self.sess.users.modify(self.new_user_name, 'password', 'blah')
        
        # try to open new session on behalf of user


        # delete user
        self.sess.users.remove(self.new_user_name)

        # user should be gone
        self.assertRaises(UserDoesNotExist, lambda: self.sess.users.get(self.new_user_name))


if __name__ == '__main__':
    # let the tests find the parent irods lib
    sys.path.insert(0, os.path.abspath('../..'))
    unittest.main()
