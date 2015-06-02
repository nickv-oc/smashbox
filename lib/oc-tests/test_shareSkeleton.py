
__doc__ = """

Test basic file sharing between users.  

+-----------+----------------------+------------------+
|  Step     |  Sharer              |  Sharee One      |
|  Number   |                      |                  |
+===========+======================+==================|
|  2        | Create work dir      |                  |
+-----------+----------------------+------------------+
|  3        | Modify welcome.txt   |                  |
+-----------+----------------------+------------------+
|  4        | Share welcome.txt    |                  |
+-----------+----------------------+------------------+
|  5        |                      | Login to create  |
|           |                      | work dir         |
+-----------+----------------------+------------------+
|  6        |                      | Syncs and        |
|           |                      | validates files  |
+-----------+----------------------+------------------+
|  7        |                      | Modifies shared  |
|           |                      | file             |
+-----------+----------------------+------------------+
|  8        | Validates modified   |                  |
|           | file                 |                  |
+-----------+----------------------+------------------+
|  9        | Sharer unshares file |                  |
+-----------+----------------------+------------------+
|  10       |                      | Syncs and        |
|           |                      | validates file   |
|           |                      | not present      |
+-----------+----------------------+------------------+
| 11        | Final step           | Final step       |
+-----------+----------------------+------------------+

"""

# from smashbox.utilities import reflection
from smashbox.utilities import *

skeletonFile = 'welcome.txt'
username1 = "%s%i" % (config.oc_account_name, 1)
username2 = "%s%i" % (config.oc_account_name, 2)


@add_worker
def setup(step):

    step(1, 'create test users')
    reset_owncloud_account(num_test_users=2, login_users=False)
    check_users(config.oc_number_test_users)

    # Login user1
    login_owncloud_account(username1, config.oc_account_password)
    #login_owncloud_account(username2, config.oc_account_password)

    reset_rundir()
    reset_server_log_file()

    step(15, 'Validate server log file is clean')
    d = make_workdir()
    scrape_log_file(d)


@add_worker
def sharer(step):

    step(2, 'Create workdir')
    d = make_workdir()
    list_files(d)
    run_ocsync(d, user_num=1)
    list_files(d)

    share_file_with_user(filename='welcome.txt', sharer=username1, sharee=username2)

    step(14, 'Sharee Two final step')


@add_worker
def sharee_one(step):

    step(3, 'Sharee creates workdir')
    d = make_workdir()
    list_files(d)

    step(4, 'Logs in')
    username2 = "%s%i" % (config.oc_account_name, 2)
    login_owncloud_account(username2, config.oc_account_password)

    run_ocsync(d, user_num=2)
    list_files(d)

    step(14, 'Sharee Two final step')
