package com.example.sidiatest;

import android.os.Bundle;
import android.util.Log;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;

import java.util.ArrayList;
import java.util.List;

import androidx.appcompat.app.AppCompatActivity;

import androidx.recyclerview.widget.DividerItemDecoration;
import androidx.recyclerview.widget.LinearLayoutManager;
import androidx.recyclerview.widget.RecyclerView;
import retrofit2.Call;
import retrofit2.Callback;
import retrofit2.Response;

public class MainActivity extends AppCompatActivity {


    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        //initializing recyclerView
        final RecyclerView mRecyclerView = (RecyclerView) findViewById(R.id.etMain_resposta);
        final LineAdapter adapter = new LineAdapter(new ArrayList<>(0));
        mRecyclerView.setHasFixedSize(true);
        mRecyclerView.setLayoutManager(new LinearLayoutManager(this));
        mRecyclerView.setAdapter(adapter);
        mRecyclerView.addItemDecoration(
                new DividerItemDecoration(this, DividerItemDecoration.VERTICAL));


        //Get text from EditText (category) and request data from the server, shows result on the recycleView.
        final EditText movieC = findViewById(R.id.etMain_movieC); //get text from EditText(category)
        Button btnBuscarMovieC = findViewById(R.id.btnMain_buscarMovieC); //button to search by category
        btnBuscarMovieC.setOnClickListener(new View.OnClickListener() {

            public void onClick(View view) {
                if (!movieC.getText().toString().equals("")) { //if its empty it does nothing
                    Call<List<Movie>> call = new RetrofitConfig().getMovieService().findMovieCat(movieC.getText().toString()); //Call servjce passing the category as parameter
                    call.enqueue(new Callback<List<Movie>>() {

                        public void onResponse(Call<List<Movie>> call, Response<List<Movie>> response) {
                            List<Movie> movie = response.body();
                            adapter.clear(); //clear recyclerView before adding more items
                            for(int i = 0; i<movie.size();i++){ //shows each result on the recycleView
                                adapter.insertItem(movie.get(i));
                            }
                        }

                        public void onFailure(Call<List<Movie>> call, Throwable t) {
                            Log.e("MovieService   ", "Error:" + t.getMessage());
                        }
                    });
                }
            }
        });

        //Get text from EditText (year) and request data from the server, shows result on the recycleView.
        final EditText movieY = findViewById(R.id.etMain_movieY); //get text from EditText(year)
        Button btnBuscarMovieY = findViewById(R.id.btnMain_buscarMovieY); //button to search by year
        btnBuscarMovieY.setOnClickListener(new View.OnClickListener() {

            public void onClick(View view) {

                if (!movieY.getText().toString().equals("")) { //check if movieY its empty
                    Call<List<Movie>> call = new RetrofitConfig().getMovieService().findMovieYear(movieY.getText().toString());//Call servjce passing the year as parameter
                    call.enqueue(new Callback<List<Movie>>() {

                        public void onResponse(Call<List<Movie>> call, Response<List<Movie>> response) {
                            List<Movie> movie = response.body();
                            adapter.clear(); //clear recyclerView before adding more items
                            for (int i = 0; i < movie.size(); i++) { //shows each result on the recycleView
                                adapter.insertItem(movie.get(i));
                            }
                        }

                        public void onFailure(Call<List<Movie>> call, Throwable t) {
                            Log.e("MovieService   ", "Erro ao buscar o filme:" + t.getMessage());
                        }
                    });
                } else { //if its empty

                    Call<List<Movie>> call = new RetrofitConfig().getMovieService().findMovie(); //call service and search for every movie
                    call.enqueue(new Callback<List<Movie>>(){

                        public void onResponse(Call<List<Movie>> call, Response<List<Movie>> response) {
                            List<Movie> movie = response.body();
                            adapter.clear(); //clear recyclerView before adding more items
                            for (int i = 0; i < movie.size(); i++) { //shows each result on the recycleView
                                adapter.insertItem(movie.get(i));
                            }
                        }

                        public void onFailure(Call<List<Movie>> call, Throwable t) {
                            Log.e("MovieService   ", "Erro ao buscar o filme:" + t.getMessage());
                        }
                    });

                }
            }
        });
    }
}