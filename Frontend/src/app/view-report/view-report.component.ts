import { Component, OnInit } from '@angular/core';
import {AuthService} from "../services/auth.service";

@Component({
  selector: 'app-view-report',
  templateUrl: './view-report.component.html',
  styleUrls: ['./view-report.component.css']
})
export class ViewReportComponent implements OnInit {
  idList: any;
  currentId: any;
  openStudentResult: boolean = false;
  checkPercentage: boolean = false;
  marksArray: any;
  finalScore: number;
  totalScore: number;
  finalMarkList:  number[] = [];
  scoreList:  number[] = [];
  finalPercentage: number;
  private multiplier: number;

  constructor(private auth: AuthService) { }

  openStudentResultDiv(){
    this.openStudentResult = true;
  }

  ngOnInit(): void {
    this.auth.get_ids_request().subscribe(response => {
      this.idList = response
      console.log(response);
    }, error => {
      // console.log(error)
    })
  }

  getResultsFromId(id: any){
    this.finalMarkList = [];
    this.scoreList = [];
    this.checkPercentage = false;
    this.auth.get_results_request(id).subscribe(response => {
      console.log(response);
      this.currentId = id;
      this.marksArray = JSON.parse(response);
      for (let entry of this.marksArray) {
        this.finalMarkList.push(parseFloat(entry.given_mark));
        this.scoreList.push(parseFloat(entry.allocated_mark));
        this.finalScore = this.finalMarkList.reduce((a, b) => a + b, 0);
        this.totalScore = this.scoreList.reduce((a, b) => a + b, 0);
      }
    }, error => {
      // console.log(error)
    })
  }

  calculatePercentage(){
    this.checkPercentage = true;
    this.finalPercentage =  (this.finalScore/ this.totalScore) * 100;
    this.multiplier = Math.pow(10, 0);
    this.finalPercentage = Math.round(this.finalPercentage * this.multiplier) / this.multiplier;
  }


}
