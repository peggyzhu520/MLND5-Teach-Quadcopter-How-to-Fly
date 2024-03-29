import numpy as np
import math
from physics_sim import PhysicsSim

class Task():
    """Task (environment) that defines the goal and provides feedback to the agent."""
    def __init__(self, init_pose=None, init_velocities=None, 
        init_angle_velocities=None, runtime=5., target_pos=None):
        """Initialize a Task object.
        Params
        ======
            init_pose: initial position of the quadcopter in (x,y,z) dimensions and the Euler angles
            init_velocities: initial velocity of the quadcopter in (x,y,z) dimensions
            init_angle_velocities: initial radians/second for each of the three Euler angles
            runtime: time limit for each episode
            target_pos: target/goal (x,y,z) position for the agent
        """
        # Simulation
        self.sim = PhysicsSim(init_pose, init_velocities, init_angle_velocities, runtime) 
        self.action_repeat = 3

        self.state_size = self.action_repeat * 6
        self.action_low = 0
        self.action_high = 900
        self.action_size = 4
      

        # Goal
        self.target_pos = target_pos if target_pos is not None else np.array([0., 0., 10.]) 

    def get_reward(self):
        """Uses current pose of sim to return reward."""
        #original settings 
        #reward = 1.-.3*(abs(self.sim.pose[:3] - self.target_pos)).sum()
        # reward trial 1 - add penalty to high speed at z
        #reward = 10 - .5*(abs(self.sim.pose[2] - self.target_pos[2])) + .3*self.sim.v[2]
        # reward trial 2, including location of x, y
        #reward = 10 - .5*(abs(self.sim.pose[2] - self.target_pos[2])) + .3*self.sim.v[2] - .2*(abs(self.sim.pose[0:2] - #self.target_pos[0:2])).sum() 
        # reward trial 3 
        #reward = 1 - .01*(abs(self.sim.pose[2] - self.target_pos[2]))**2 - .003*abs(self.sim.v[2])**2 - .1*#(abs(self.sim.pose[0:2] - self.target_pos[0:2])).sum() - 0.00005*(self.sim.v[0]**2+ self.sim.v[1]**2 )
       # trial 4
        #if self.sim.pose[2] >0:
           # reward = 1 - .3*(abs(self.sim.pose[2] - self.target_pos[2])) - .003*abs(self.sim.v[2])**2
       # else:
           # reward = 1 - .01*(abs(self.sim.pose[2] - self.target_pos[2]))**2 - .003*abs(self.sim.v[2])**2 - .1*(abs(self.sim.pose[0:2] - self.target_pos[0:2])).sum() - 0.00005*(self.sim.v[0]**2+ self.sim.v[1]**2 )

 #       return reward
    # trial  5
        #if self.sim.pose[2] >0:
           # reward = 1 - .3*(abs(self.sim.pose[2] - self.target_pos[2])) - .003*abs(self.sim.v[2])**2
        #if self.sim.pose[2] == 0:
          #  reward = 10 - .003*abs(self.sim.v[2]) - .1*(abs(self.sim.pose[0:2] - self.target_pos[0:2])).sum() - 0.00005*(self.sim.v[0]**2+ self.sim.v[1]**2 )
      #  else:
           # reward -= 5
       # return reward
    
    # trial 8
        #reward = 1 - .01*(abs(self.sim.pose[2] - self.target_pos[2]))**2 - .003*abs(self.sim.v[2])**2 - .1*(abs(self.sim.pose[0:2] - self.target_pos[0:2])).sum() - 0.00005*(self.sim.v[0]**2+ self.sim.v[1]**2 )
        #if self.sim.time < self.sim.runtime and self.sim.done == True:
          #  reward -= 5
        #trial remove reward for continuing flying
        #reward =  1 - .3*(abs(self.sim.pose[2] - self.target_pos[2])) - .003*abs(self.sim.v[2])**2 - .1*(abs(self.sim.pose[0:2] #- self.target_pos[0:2])).sum() - 0.00005*(self.sim.v[0]**2+ self.sim.v[1]**2 )
      #  if self.sim.time < self.sim.runtime and self.sim.done == True:
         #   reward -= 5
        
        
            # trial 9
        #reward =  1 - .3*(abs(self.sim.pose[2] - self.target_pos[2])) - .003*abs(self.sim.v[2])**2 - .1*(abs(self.sim.pose[0:2] - self.target_pos[0:2])).sum() - 0.00005*(self.sim.v[0]**2+ self.sim.v[1]**2 )
       # if self.sim.time < self.sim.runtime and self.sim.done == True:
         #   reward -= 5
        #if abs(self.sim.v[2]) > 5:
         #   reward -= 2
        
            # trial 10
        '''reward =  1 - .5*(abs(self.sim.pose[2] - self.target_pos[2])) -.3*abs(self.sim.v[2])
        if self.sim.time < self.sim.runtime and self.sim.done == True:
            reward -= 2'''
 
          # trial 11 
        '''if self.sim.pose[2] == self.target_pos[2]:
            if self.sim.v[2] < 1:
                if (self.sim.pose[0] < 0.5) and (self.sim.pose[1] < 0.5):
                    reward =10 
                else: reward = -1 # land too far away from the landing zone
            else: reward = -10  #too high speed, hence not landing softly
        else:
            #to encourage approaching to landing zone
            reward =  1 -  (abs(self.sim.pose[2] - self.target_pos[2])/10)'''
        # trial 12
        dist_reward = 1 - 0.1*abs(self.sim.pose[2] - self.target_pos[2])
        vel_discount = 1/max(abs(self.sim.v[2]),0.001)
        reward = dist_reward*vel_discount
        # trial 15
        '''dist_reward = 1 - np.tanh(abs(self.sim.pose[2] - self.target_pos[2]))
        vel_discount = 1/max(abs(self.sim.v[2]),0.001)
        reward = dist_reward*vel_discount'''
        # trial 16
        '''dist_reward = 1 - np.tanh(abs(self.sim.pose[2] - self.target_pos[2]))
        vel_discount = 1 - np.tanh(abs(self.sim.v[2]))
        reward = dist_reward*vel_discount'''
        
        # trial 17
        '''dist_reward = 1 - np.tanh(abs(self.sim.pose[2] - self.target_pos[2]))
        vel_discount = 2 - math.log10(abs(self.sim.v[2]+1))
        reward = dist_reward*vel_discount'''
        # trial 18 
        '''reward = 1 - np.tanh(abs(self.sim.pose[2] - self.target_pos[2])) - np.tanh(abs(self.sim.v[2]))'''
        return reward


    def step(self, rotor_speeds):
        """Uses action to obtain next state, reward, done."""
        reward = 0
        pose_all = []
        for _ in range(self.action_repeat):
            done = self.sim.next_timestep(rotor_speeds) # update the sim pose and velocities
            reward += self.get_reward() 
            pose_all.append(self.sim.pose)
        next_state = np.concatenate(pose_all)
        return next_state, reward, done

    def reset(self):
        """Reset the sim to start a new episode."""
        self.sim.reset()
        state = np.concatenate([self.sim.pose] * self.action_repeat) 
        return state