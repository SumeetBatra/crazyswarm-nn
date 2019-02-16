#include <iostream>
#include <chrono>

// #include <ros/ros.h>

// Motion Capture
// #ifdef ENABLE_VICON
#include <libmotioncapture/vicon.h>
// #endif
// #ifdef ENABLE_OPTITRACK
// #include <libmotioncapture/optitrack.h>
// #endif
// #ifdef ENABLE_PHASESPACE
// #include <libmotioncapture/phasespace.h>
// #endif

static inline float fsqr(float x) { return x * x; }

int main(int argc, char **argv)
{
//   ros::init(argc, argv, "record_pose");

//   ros::NodeHandle nl("~");

//   std::string motionCaptureType;
//   nl.param<std::string>("motion_capture_type", motionCaptureType, "vicon");

//   // Make a new client
//   libmotioncapture::MotionCapture* mocap = nullptr;
//   if (false)
//   {
//   }
// #ifdef ENABLE_VICON
//   else if (motionCaptureType == "vicon")
//   {
//     std::string hostName;
//     nl.getParam("vicon_host_name", hostName);
//     mocap = new libmotioncapture::MotionCaptureVicon(hostName,
//       /*enableObjects*/ false,
//       /*enablePointcloud*/ true);
//   }
// #endif
// #ifdef ENABLE_OPTITRACK
//   else if (motionCaptureType == "optitrack")
//   {
//     std::string localIP;
//     std::string serverIP;
//     nl.getParam("optitrack_local_ip", localIP);
//     nl.getParam("optitrack_server_ip", serverIP);
//     mocap = new libmotioncapture::MotionCaptureOptitrack(localIP, serverIP);
//   }
// #endif
// #ifdef ENABLE_PHASESPACE
//   else if (motionCaptureType == "phasespace")
//   {
//     std::string ip;
//     int numMarkers;
//     nl.getParam("phasespace_ip", ip);
//     nl.getParam("phasespace_num_markers", numMarkers);
//     std::map<size_t, std::pair<int, int> > cfs;
//     cfs[231] = std::make_pair<int, int>(10, 11);
//     mocap = new libmotioncapture::MotionCapturePhasespace(ip, numMarkers, cfs);
//   }
// #endif
//   else {
//     throw std::runtime_error("Unknown motion capture type!");
//   }

  libmotioncapture::MotionCapture* mocap = new libmotioncapture::MotionCaptureVicon("vicon",
      /*enableObjects*/ true,
      /*enablePointcloud*/ false);

  // pcl::PointCloud<pcl::PointXYZ>::Ptr markers(new pcl::PointCloud<pcl::PointXYZ>);
  libmotioncapture::Object object;

  std::cout << "time,x,y,z,qx,qy,qz,qw,roll,pitch,yaw" << std::endl;

  auto startTime = std::chrono::high_resolution_clock::now();

  for (size_t frameId = 0; ; ++frameId) {
    // std::cout << "frame " << frameId << ":" << std::endl;
    // Get a frame
    mocap->waitForNextFrame();

    auto time = std::chrono::high_resolution_clock::now();
    std::chrono::duration<double> elapsedSeconds = time-startTime;

    mocap->getObjectByName("cf2", object);
    
    if (!object.occluded()) {

      // auto euler = object.rotation().toRotationMatrix().eulerAngles(0, 1, 2);
      const auto& q = object.rotation();

      double roll = atan2(2 * (q.w() * q.x() + q.y() * q.z()), 1 - 2 * (fsqr(q.x()) + fsqr(q.y()))); // roll
      double pitch = asin(2 * (q.w() * q.y() - q.x() * q.z())); // pitch
      double yaw = atan2(2 * (q.w() * q.z() + q.x() * q.y()), 1 - 2 * (fsqr(q.y()) + fsqr(q.z()))); // yaw

      std::cout << elapsedSeconds.count() << ",";
      std::cout << object.position().x() << ",";
      std::cout << object.position().y() << ",";
      std::cout << object.position().z() << ",";
      std::cout << object.rotation().x() << ",";
      std::cout << object.rotation().y() << ",";
      std::cout << object.rotation().z() << ",";
      std::cout << object.rotation().w() << ",";
      std::cout << roll << ",";
      std::cout << pitch << ",";
      std::cout << yaw;
      std::cout << std::endl;
    }

    if (elapsedSeconds.count() >= 10.0) {
      break;
    }

    // ros::spinOnce();
  }

  return 0;
}
