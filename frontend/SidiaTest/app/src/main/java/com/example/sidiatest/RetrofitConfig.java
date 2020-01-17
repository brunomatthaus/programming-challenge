package com.example.sidiatest;

import java.util.concurrent.TimeUnit;

import okhttp3.OkHttpClient;
import retrofit2.Retrofit;
import retrofit2.converter.jackson.JacksonConverterFactory;

public class RetrofitConfig {

//retrofit configuration

    private final Retrofit retrofit;

    public RetrofitConfig() {

        OkHttpClient okHttpClient = new OkHttpClient().newBuilder()
                .connectTimeout(60, TimeUnit.SECONDS)
                .readTimeout(60, TimeUnit.SECONDS)
                .writeTimeout(60, TimeUnit.SECONDS)
                .retryOnConnectionFailure(true)
                .build();


        this.retrofit = new Retrofit.Builder()
                .baseUrl("http://10.0.2.2:5000/")
                .client(okHttpClient)
                .addConverterFactory(JacksonConverterFactory.create())
                .build();
    }

    public MovieService getMovieService() {
        return this.retrofit.create(MovieService.class);
    }


}
