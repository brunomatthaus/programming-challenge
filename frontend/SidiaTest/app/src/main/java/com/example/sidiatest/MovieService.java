package com.example.sidiatest;

import java.util.List;

import retrofit2.Call;
import retrofit2.http.GET;
import retrofit2.http.Path;

public interface MovieService {

//GET + endpoints

    @GET("movies/{category}")
    Call<List<Movie>> findMovieCat(@Path("category") String category);

    @GET("ranking/{year}")
    Call<List<Movie>> findMovieYear(@Path("year") String year);

    @GET("ranking")
    Call<List<Movie>> findMovie();

}
