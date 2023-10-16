from fastapi import  status, HTTPException, Depends, APIRouter, Response
from .. import  models, schemas, oauth2
from sqlalchemy.orm import Session
from ..database import  get_db
from typing import  List, Optional
from app import database

router = APIRouter(prefix= '/vote', tags=['vote'])

@router.post("/", status_code= status.HTTP_201_CREATED)
def vote(vote: schemas.Vote, db: Session = Depends(database.get_db), current_user: int = Depends(oauth2.get_current_user)):
    # vote_query = db.query(models.Vote).filter(models.Vote.post_id==vote.post_id, models.Vote.user_id == current_user.id) 
    # found_vote = vote_query.first()
    # if (vote.dir ==1):
    #     if found_vote:
    #        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f'user {current_user.id} has already voted on the post {vote.post_id}')
    #     new_vote = models.Vote(post_id = vote.post_id, user_id =current_user.id)
    #     db.add(new_vote)
    #     db.commit() 
    #     return {'message':'successfuly voted'}  
    # else: 
    #     if not found_vote:
    #         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='post does not exist')
    #     vote_query.delete(synchronize_session=False)
    #     db.commit()
    post = db.query(models.Post).filter(models.Post.id == vote.post_id).first()
    
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Post does not exist')

    vote_query = db.query(models.Vote).filter(models.Vote.post_id == vote.post_id, models.Vote.user_id == current_user.id)
    found_vote = vote_query.first()

    if vote.dir == 1:
        if found_vote:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f'user {current_user.id} has already voted on the post {vote.post_id}')
        new_vote = models.Vote(post_id=vote.post_id, user_id=current_user.id)
        db.add(new_vote)
        db.commit()
        return {'message': 'Successfully voted'}
    else:
        if not found_vote:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='You cannot delete a vote that does not exist')
        vote_query.delete(synchronize_session=False)
        db.commit()
        return {'message': 'Successfully deleted vote'}


