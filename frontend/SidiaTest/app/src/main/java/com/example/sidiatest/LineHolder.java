package com.example.sidiatest;

import android.view.View;
import android.widget.TextView;

import androidx.recyclerview.widget.RecyclerView;

public class LineHolder extends RecyclerView.ViewHolder {


//recycle view line configuration (shows each result of movies searches)

    public TextView tconst;
    public TextView primaryTitle;
    public TextView originalTitle;
    public TextView startYear;
    public TextView averageRating;
    public TextView numVotes;

    public LineHolder(View itemView) {
        super(itemView);
        tconst = (TextView) itemView.findViewById(R.id.main_line_tconst);
        primaryTitle = (TextView) itemView.findViewById(R.id.main_line_primaryTitle);
        originalTitle = (TextView) itemView.findViewById(R.id.main_line_originalTitle);
        startYear = (TextView) itemView.findViewById(R.id.main_line_startYear);
        averageRating = (TextView) itemView.findViewById(R.id.main_line_averageRating);
        numVotes = (TextView) itemView.findViewById(R.id.main_line_numVotes);
    }
}