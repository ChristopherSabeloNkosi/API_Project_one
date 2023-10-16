from fastapi import  status, HTTPException, Depends, APIRouter, Response
from sqlalchemy import func
from .. import  models, schemas, oauth2
from sqlalchemy.orm import Session
from ..database import  get_db
from typing import  List, Optional
from sqlalchemy.orm import aliased

router =APIRouter(prefix='/posts', tags= ['Posts'])

@router.get("/", response_model=List[schemas.Post])
def get_posts(db: Session = Depends(get_db),current_user: int = Depends(oauth2.get_current_user),limit: int = 10, search: Optional[str] = ""):
    #  posts = db.query(models.Post).filter(models.Post.owner_id ==current_user.id).all()
    # posts = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).all()
    
   posts = db.query(
        models.Post,
        func.count(models.Vote.post_id).label('votes'),
        models.User.email
    ) \
    .join(models.Vote, models.Vote.post_id == models.Post.id, isouter=True) \
    .join(models.User, models.User.id == models.Post.owner_id) \
    .group_by(models.Post.id, models.User.email) \
    .filter(models.Post.title.contains(search)) \
    .limit(limit) \
    .all()
   
    
   posts_with_vote_counts = [
        schemas.Post(
            id=post[0].id,
            title=post[0].title,
            content=post[0].content,
            published = post[0].published,
            created_at=post[0].created_at,
            posted_by=post[2],
            votes=post[1] if post[1] is not None else 0
        )
        for post in posts
    ]

   return posts_with_vote_counts
    
    # cursor.execute('''SELECT * FROM "Posts"''')
    # posts = cursor.fetchall()
    # return {'data': posts}


@router.post('/createpost', status_code= status.HTTP_201_CREATED, response_model= schemas.Post )
def create_post(post: schemas.PostCreate, db: Session = Depends(get_db),current_user: int = Depends(oauth2.get_current_user)):
    
    new_post = models.Post(owner_id = current_user.id, **post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post
    # cursor.execute('''INSERT INTO "Posts" (title,content, published)
    #                VALUES  (%s,%s,%s)
    #                RETURNING *''',(post.tittle,post.contents,post.published))
    # # cursor.execute('''INSERT INTO Posts" (title,content,published) VALUES (%s,%s,%s) RETURNING'''
    # #                ,(post.tittle,post.contents,post.published))
    # new_post = cursor.fetchone()
    # conn.commit()
    # new_post = models.Post(title=post.tittle, content=post.contents, published= post.published)
   


@router.get("/{id}", response_model= schemas.Post)
def get_post_by_id(id: int, db: Session = Depends(get_db),current_user: int = Depends(oauth2.get_current_user)):
    # post = db.query(models.Post).filter(models.Post.id == current_user.id).first()
    post = db.query(
        models.Post,
        func.count(models.Vote.post_id).label('votes'),
        models.User.email
    ) \
    .join(models.Vote, models.Vote.post_id == models.Post.id, isouter=True) \
    .join(models.User, models.User.id == models.Post.owner_id) \
    .group_by(models.Post.id, models.User.email) \
    .filter(models.Post.id == id).first()
    if not post:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f'post with id: {id} was not found')
    
    posts_with_vote_counts = schemas.Post(
            id=post[0].id,
            title=post[0].title,
            content=post[0].content,
            published = post[0].published,
            created_at=post[0].created_at,
            posted_by=post[2],
            votes=post[1] if post[1] is not None else 0
        )
        
    

    return posts_with_vote_counts


 # cursor.execute('''SELECT * FROM "Posts" WHERE id = %s''',(str(id),))
    # post = cursor.fetchone()

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int,db: Session = Depends(get_db),current_user: int = Depends(oauth2.get_current_user)):
    delete_query = db.query(models.Post).filter(models.Post.id == id)
    deleted_post = delete_query.first()
    if deleted_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'post with id: {id} was not found')
    
    if deleted_post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f'Not authorized to perform requested action')
    delete_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

    # cursor.execute('''DELETE FROM "Posts" WHERE id = %s returning *''',(str(id),))
    # deleted_post = cursor.fetchone()
    # conn.commit()
    
@router.put("/{id}", response_model= schemas.Post)
def update_post(id:int, updated_post:schemas.PostCreate, db: Session = Depends(get_db),current_user: int = Depends(oauth2.get_current_user)):
    post_query= db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()
    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'post with id: {id} was not found')
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f'Not authorized to perform requested action')
    post_query.update(updated_post.dict(), synchronize_session=False)
    db.commit()
    return  post_query.first()
    # cursor.execute('''UPDATE "Posts" SET title= %s, content= %s, published= %s WHERE id = %s returning *'''),(post.tittle, post.contents, post.published, (str(id),))
    # cursor.execute('''UPDATE "Posts" 
    #                   SET title = %s, content = %s, published = %s
    #                   WHERE id = %s
    #                   RETURNING *''', (post.tittle, post.contents, post.published, (str(id),)))
    # updated_post = cursor.fetchone()
    # conn.commit()
