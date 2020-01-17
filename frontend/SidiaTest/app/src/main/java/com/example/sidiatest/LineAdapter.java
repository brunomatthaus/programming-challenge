package com.example.sidiatest;

import android.view.LayoutInflater;
import android.view.ViewGroup;

import java.util.ArrayList;
import java.util.List;
import java.util.Locale;

import androidx.recyclerview.widget.RecyclerView;


public class LineAdapter extends RecyclerView.Adapter<LineHolder> {

//adapter to control the recycleView that displays the searches results

    private final List<Movie> mMovie;

    public LineAdapter(ArrayList movies) {
        mMovie = movies;
    }

    @Override
    public LineHolder onCreateViewHolder(ViewGroup parent, int viewType) {
        return new LineHolder(LayoutInflater.from(parent.getContext())
                .inflate(R.layout.main_line_view, parent, false));
    }

    @Override
    public void onBindViewHolder(LineHolder holder, int position) {
        holder.tconst.setText(String.format(Locale.getDefault(), "%s",
                "tconst: "+mMovie.get(position).getTCONST()
        ));
        holder.primaryTitle.setText(String.format(Locale.getDefault(), "%s",
                "Primary Title: "+mMovie.get(position).getPRIMARYTITLE()
        ));
        holder.originalTitle.setText(String.format(Locale.getDefault(), "%s",
                "Original Title: "+mMovie.get(position).getORIGINALTITLE()
        ));
        holder.startYear.setText(String.format(Locale.getDefault(), "%s",
                "Start Year: "+mMovie.get(position).getSTARTYEAR()
        ));
        holder.averageRating.setText(String.format(Locale.getDefault(), "%s",
                "Average Rating: "+mMovie.get(position).getAVERAGERATING()
        ));
        holder.numVotes.setText(String.format(Locale.getDefault(), "%s",
                "Number of Votes: "+mMovie.get(position).getNUMVOTES()
        ));

    }

    @Override
    public int getItemCount() {
        return mMovie != null ? mMovie.size() : 0;
    }


    //clear recyclerView
    public void clear() {
        mMovie.clear();
        notifyDataSetChanged();
    }

    //insert item in recyclerView
    public void insertItem(Movie movie) {
        mMovie.add(movie);
        notifyItemInserted(getItemCount());
    }
}