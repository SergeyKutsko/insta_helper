# Instargam Helper
....................................
# How to run a project on your local machine?
1.Install Docker https://docs.docker.com/engine/install/    
2.Run make build c=pgadmin    
3.Open http://localhost:5050/browser/ with password: insta_helper_dev and create DB insta_helper_dev    
4.Run make build - If you have error /data/db: permission denied failed to solve run: sudo chmod -R 777 ./data/db  
5.Run migrations by docker exec -it insta_helper_dev python3 manage.py migrate (makemigrations for next steps)   
6.Run docker exec -it insta_helper_dev python3 manage.py createsuperuser    
7.Open http://localhost/admin/ in browser and auth with user created at step 6   
8.Run docker exec -it insta_helper_web python3 manage.py runscript limits    


