import { Component, OnInit } from '@angular/core';
import {AuthService} from "../services/auth.service";

@Component({
  selector: 'app-feedback',
  templateUrl: './feedback.component.html',
  styleUrls: ['./feedback.component.css']
})
export class FeedbackComponent implements OnInit {
  evaluationResults: any;
  resultsArray: any;

  constructor(private auth: AuthService) { }

  ngOnInit(): void {
    this.evaluationResults = this.auth.getData();

    this.resultsArray = JSON.parse(this.evaluationResults);
    console.log(this.resultsArray.final_mark)
    console.log(this.resultsArray.required_keywords)
    console.log(this.resultsArray.matched_keyword)
    console.log(this.evaluationResults.keyword_similarity_score)

  }

  scrollToTop(){
    window.scroll(0,0);
  }

}
