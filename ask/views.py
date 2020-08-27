from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from accounts.models import Account, Category
from accounts.serializers import AccountShowSerializer, CategorySerializer, CategoryUserSerializer

from .serializers import QuestionSerializer, AnswerSerializer
from .models import Question, Answer

import json

@api_view(['POST'])
def ask_question(request, username):
    # check if the username is exists in the database ..
    try:
        user = Account.objects.get(username=username)
    except:
        # if username does not exist in the database 
        # return reponse 404 not found 
        return Response({}, status=status.HTTP_404_NOT_FOUND)
    # get the current user
    current_user = request.user

    # create a new question 
    Question.objects.create(
        author=current_user,
        to=user,
        body=request.data.get('body')
    )
    return Response({}, status=status.HTTP_201_CREATED)

@api_view(['POST'])
def answer_question(request):
    # get the question id 
    question_id = request.data.get('question_id')
    # get the question object by question_id
    try:
        question_object = Question.objects.get(id=question_id)
    except:
        # if question object does not exist ..
        # return 404 not found
        return Response({}, status=status.HTTP_404_NOT_FOUND)

    if request.user != question_object.to:
        return Response({}, status='400')

    # Answer to the question 
    Answer.objects.create(
        question=question_object,
        author=request.user,
        body=request.data.get('body')
    )
    # change the bool field of is_answered to be true
    question_object.is_answered = True
    question_object.save()

    # return response with 201 created
    return Response({}, status=status.HTTP_201_CREATED)

@api_view(['POST'])
def toggle_follow(request, username):
    
    try:
        # get the Account object by username
        user = Account.objects.get(username=username)
    except Account.DoesNotExists:
        # if user does not exist in the database ...
        # return response 404 not found 
        return Response({}, status=status.HTTP_404_NOT_FOUND)

    # get the currrent user 
    current_user = request.user

    # check if the user in the following list 
    if user in current_user.following.all():
        # if the user exists in the following list 
        # remove user from the following list  
        current_user.following.remove(user)
        # return response 
        return Response({}, status=status.HTTP_200_OK)
    else:
        # if the user does not exist in the following list ...
        # add user to the following list
        current_user.following.add(user)
        # return response 
        return Response({}, status=status.HTTP_201_CREATED)

@api_view(['GET'])
def get_all_questions(request):
    # get the current user 
    current_user = request.user
    
    # check if the user asked questions
    # the questions have not any answers
    # these questions needs to be answered by someone 
    questions_needs_answers = Question.objects.filter(author=current_user, is_answered=False)
    
    # check if user has answered questions 
    # these questions already have answers so it does not need to be answered by someone
    answered_questions = Question.objects.filter(author=current_user, is_answered=True)
    # use serializer to serializer data
    questions_needs_answers_serializer = QuestionSerializer(questions_needs_answers, many=True)
    answered_questions_serializer = QuestionSerializer(answered_questions, many=True)
    return Response({
        'questions_needs_answer' : questions_needs_answers_serializer.data,
        'answered_questions': answered_questions_serializer.data
    }, status=status.HTTP_200_OK)

@api_view(['GET'])
def get_all_answers(request):
    # get the current user
    current_user = request.user 

    # get all answers of the current user 
    all_answers = Answer.objects.filter(author=current_user)

    # serilaize data of the all_answers 
    # convert data to JSON
    all_answers_serializer = AnswerSerializer(all_answers, many=True)

    return Response({
       'all_answers': all_answers_serializer.data  
    }, status=status.HTTP_200_OK)

@api_view(['GET'])
def get_all_categories(request):
    all_categories = Category.objects.all()
    serializer = CategorySerializer(all_categories, many=True)
    return Response({'data': serializer.data }, status=status.HTTP_200_OK)

@api_view(['POST'])
def add_category_to_user(request):

    categories = request.data.get('data')
    current_user = request.user

    for category in categories:

        new_category = Category.objects.filter(category_name=category).first()
        if get_category:
            current_user.category.add(new_category)
    
    
    return Response({}, status=status.HTTP_200_OK)

@api_view(['GET'])
def get_all_categories_of_current_user(request):
    
    # get current user 
    current_user = request.user

    # get all categories that the current user in it 
    all_categories = current_user.category.all()
    serializer = CategorySerializer(all_categories, many=True)
    return Response({
        'data': serializer.data
    }, status=status.HTTP_200_OK)

@api_view(['GET'])
def get_mutual_categories(request):
    
    # get current user 
    current_user = request.user

    # get all categories that the current user in it 
    all_categories = current_user.category.all()
    serializer = CategoryUserSerializer(all_categories, many=True)
    return Response({
        'data': serializer.data
    }, status=status.HTTP_200_OK)

