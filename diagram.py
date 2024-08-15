from diagrams import Cluster, Diagram, Edge
from diagrams.onprem.analytics import Spark
from diagrams.onprem.compute import Server
from diagrams.onprem.database import MySQL
from diagrams.onprem.inmemory import Redis
from diagrams.onprem.aggregator import Fluentd
from diagrams.onprem.monitoring import Nagios
from diagrams.onprem.network import Nginx
from diagrams.onprem.queue import Kafka
from diagrams.onprem.client import Users
from diagrams.elastic.saas import Elastic
from diagrams.custom import Custom
from diagrams.generic.compute import Rack
from diagrams.onprem.vcs import Github
from diagrams.aws.network import ALB
from diagrams.aws.compute import EC2
from diagrams.aws.database import RDSPostgresqlInstance 
from diagrams.aws.management import Cloudwatch
from diagrams.aws.storage import S3, Backup
from diagrams.aws.engagement  import SES

with Diagram("Liferay Reference Archtecture On-Prem",  filename="diagram", show=False):
    users = Users("users")
    github = Github("Repository")

    with Cluster("Private Network"):
        ingress = ALB("Load Balancer")
        metrics = Cloudwatch("metrics")
        backup = Backup("Backup")
        mailsvc = SES("Email Service")

        with Cluster("Liferay Cluster"):
            lrsvc = [EC2("Liferay Node1"), EC2("Liferay Node2")]

        with Cluster("Database Cluster"):
            dbs = RDSPostgresqlInstance("Master and slave")
            lrsvc >> dbs >> metrics

        with Cluster("Elasticsearch Cluster"):
            elks = Elastic("3 servers on EC2")
            lrsvc >> elks >> metrics      

        with Cluster("File Server"):
            nfs = S3("Documents and Media")
            lrsvc >> nfs >> metrics    

    users >> ingress >> lrsvc
    lrsvc - backup
    nfs - backup
    lrsvc - mailsvc
    github >> Edge(label="Deploy") >> lrsvc