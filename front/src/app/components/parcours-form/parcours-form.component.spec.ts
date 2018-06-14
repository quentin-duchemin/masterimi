import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { ParcoursFormComponent } from './parcours-form.component';

describe('ParcoursFormComponent', () => {
  let component: ParcoursFormComponent;
  let fixture: ComponentFixture<ParcoursFormComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ ParcoursFormComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(ParcoursFormComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
