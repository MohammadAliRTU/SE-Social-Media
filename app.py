from flask import Flask, render_template, request, redirect, url_for, flash, session
import requests
import random

app = Flask(__name__)

@app.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        username = request.form['username']
        common_id = random.randint(10000, 999999)
        name = request.form['name']
        city = request.form['city']
        age = request.form['age']
        session['common_id'] = common_id

        form_data = {
            "data": {
                "email": email,
                "password": password,
                "username": username,
                "common_id": common_id,
                "name": name,
                "city": city,
                "age": age
            }
        }

        response = requests.post('http://127.0.0.1:8000/sign-up', json=form_data)
        
        if response.status_code == 200:
            flash('User added to the system successfully', 'success')
            return redirect(url_for('feed_page'))
        else:
            flash('Email address or password is not valid', 'danger')
    
    return render_template('sign_up.html')

@app.route('/sign-in', methods=['GET', 'POST'])
def sign_in():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        
        form_data = {
            "data": {
                "email": email,
                "password": password,
            }
        }
        
        response = requests.post('http://127.0.0.1:8000/sign-in', json=form_data)
        
        if response.status_code == 200:
            flash('User signed in successfully', 'success')
            response_data = response.json()
            session['common_id'] = response_data['data']
            return redirect(url_for('feed_page'))
        else:
            flash('Email address or password is not valid', 'danger')
    
    return render_template('sign_in.html')

@app.route('/follow', methods=['GET', 'POST'])
def follow():
    if request.method == 'POST':
        common_id = session.get('common_id')
        following_id = request.form['following_id']

        if not common_id:
            return redirect(url_for('sign_in'))
        
        form_data = {
            "data": {
                "follower_common_id": common_id,
                "following_common_id": int(following_id)
            }
        }
        
        response = requests.post('http://127.0.0.1:8000/follow', json=form_data)
        
        if response.status_code == 200:
            flash('Started following user successfully', 'success')
            return redirect(url_for('feed_page'))
        else:
            flash('Already following', 'danger')
    
    return render_template('search_results.html')

@app.route('/feed-page', methods=['GET', 'POST'])
def feed_page():
    common_id = session.get('common_id')

    if not common_id:
        return redirect(url_for('sign_in'))

    form_data = {
        "data": {
            "common_id": common_id
        }
    }
    
    response = requests.post('http://127.0.0.1:8000/feed-page', json=form_data)
    
    if response.status_code == 200:
        response_data = response.json()
        feed_data = response_data['data']
        print(feed_data['tweets'])
        print("feed data: ", feed_data)
        return render_template('feed_page.html', feed_data=feed_data)
    else:
        flash('Failed to load feed', 'danger')
    
    return render_template('feed_page.html', feed_data={})

@app.route('/make-tweet', methods=['GET', 'POST'])
def make_tweet():
    if request.method == 'POST':
        tweet_content = request.form['tweet_content']
        common_id = session.get('common_id')

        if not common_id:
            return redirect(url_for('sign_in'))
        
        form_data = {
            "data": {
                "common_id": common_id,
                "tweet": tweet_content
            }
        }

        response = requests.post('http://127.0.0.1:8000/tweet', json=form_data)
        

        if response.status_code == 200:
            flash('Tweet posted successfully', 'success')
            return redirect(url_for('feed_page'))
        else:
            flash('Failed to post tweet', 'danger')
    
    return render_template('make_tweet.html')


@app.route('/search-results', methods=['GET', 'POST'])
def search_results():
    username = request.form['search_query']
    
    form_data = {
        "data": {
            "username": username
        }
    }
    
    response = requests.post('http://127.0.0.1:8000/search-username', json=form_data)
    
    if response.status_code == 200:
        search_results_data = response.json()
        search_results = search_results_data['data']
        print(search_results)

        return render_template('search_results.html', search_query=username, results=search_results)
    else:
        flash('Search failed', 'danger')
        return redirect(url_for('feed_page'))

@app.route('/logout', methods=['GET', 'POST'])
def logout():
    session.clear()
    
    return redirect(url_for('sign_in'))

if __name__ == '__main__':
    app.run(debug=True)
