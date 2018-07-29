from tornado.options import define, options, parse_command_line # tornado options related imports


COOKIE_SECRET = 'roshan'
define("port", default=8888, help="run on the given port", type=int)
define("db_connection_str", default="mysql://root:password@db/octopuslabs", help="Database connection string for application") # db connection string
define("executor_max_threads", default=20, help="max threads for threadpool executor") # max number of threads for executor

parse_command_line() # firstly, get the above options from command line