# Instargam Helper
....................................
# How to run a project on your local machine?
1.Install Docker https://docs.docker.com/engine/install/    
2.Run make c=pgadmin    
3.Open http://localhost:5050/browser/ with password: insta_helper_dev and create DB insta_helper_dev    
4.Run make build - If you have error /data/db: permission denied failed to solve run: sudo chmod -R 777 ./data/db  
5.Run migrations by docker exec -it insta_helper_dev python3 manage.py migrate    
6.Run migrations by docker exec -it insta_helper_dev python3 manage.py createsuperuser
7.Open http://localhost/admin/ in browser and auth with user created at step 6

